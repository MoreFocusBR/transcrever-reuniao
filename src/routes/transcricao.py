import os
import json
import tempfile
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import whisper
from pydub import AudioSegment
from datetime import datetime
import re

transcricao_bp = Blueprint('transcricao', __name__)

# Configurações
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'m4a', 'mp3', 'wav', 'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_wav(input_path, output_path):
    """Converte arquivo de áudio para WAV"""
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="wav")
        return True
    except Exception as e:
        print(f"Erro na conversão: {e}")
        return False

def identify_speakers(segments):
    """Identifica falantes baseado em pausas e mudanças de tom"""
    speakers = []
    current_speaker = 1
    last_end_time = 0
    
    for segment in segments:
        # Se há uma pausa longa (>2 segundos), pode ser um novo falante
        if segment['start'] - last_end_time > 2.0:
            current_speaker += 1
        
        speakers.append({
            'speaker_id': f"Falante {current_speaker}",
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text'].strip()
        })
        
        last_end_time = segment['end']
    
    return speakers

def generate_summary(transcription_data):
    """Gera resumo dos pontos principais da reunião"""
    all_text = " ".join([item['text'] for item in transcription_data])
    
    # Identifica palavras-chave relacionadas a reuniões de trabalho
    keywords = [
        'decisão', 'decidir', 'combinado', 'acordo', 'definir',
        'prazo', 'deadline', 'entrega', 'responsável', 'tarefa',
        'próxima', 'semana', 'reunião', 'ação', 'pendência',
        'projeto', 'meta', 'objetivo', 'resultado'
    ]
    
    sentences = re.split(r'[.!?]+', all_text)
    important_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20:  # Ignora frases muito curtas
            for keyword in keywords:
                if keyword.lower() in sentence.lower():
                    important_sentences.append(sentence)
                    break
    
    return {
        'pontos_principais': important_sentences[:10],  # Máximo 10 pontos
        'total_falantes': len(set([item['speaker_id'] for item in transcription_data])),
        'duracao_total': max([item['end'] for item in transcription_data]) if transcription_data else 0
    }

@transcricao_bp.route('/upload', methods=['POST'])
def upload_audio():
    """Endpoint para upload e transcrição de arquivo de áudio"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Formato de arquivo não suportado'}), 400
        
        # Criar diretório de upload se não existir
        upload_dir = os.path.join(current_app.root_path, UPLOAD_FOLDER)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Salvar arquivo
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)
        
        # Converter para WAV se necessário
        wav_path = filepath
        if not filename.lower().endswith('.wav'):
            wav_path = filepath.rsplit('.', 1)[0] + '.wav'
            if not convert_to_wav(filepath, wav_path):
                return jsonify({'error': 'Erro na conversão do arquivo'}), 500
        
        # Carregar modelo Whisper
        model = whisper.load_model("base")
        
        # Transcrever áudio
        result = model.transcribe(wav_path, language='pt')
        
        # Identificar falantes
        speakers_data = identify_speakers(result['segments'])
        
        # Gerar resumo
        summary = generate_summary(speakers_data)
        
        # Limpar arquivos temporários
        if os.path.exists(filepath):
            os.remove(filepath)
        if wav_path != filepath and os.path.exists(wav_path):
            os.remove(wav_path)
        
        return jsonify({
            'success': True,
            'transcricao': speakers_data,
            'resumo': summary,
            'texto_completo': result['text']
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500

@transcricao_bp.route('/update-speakers', methods=['POST'])
def update_speakers():
    """Endpoint para atualizar nomes dos falantes"""
    try:
        data = request.get_json()
        transcricao = data.get('transcricao', [])
        speaker_names = data.get('speaker_names', {})
        
        # Atualizar nomes dos falantes
        for item in transcricao:
            old_speaker_id = item['speaker_id']
            if old_speaker_id in speaker_names:
                item['speaker_id'] = speaker_names[old_speaker_id]
        
        # Regenerar resumo com nomes atualizados
        summary = generate_summary(transcricao)
        
        return jsonify({
            'success': True,
            'transcricao': transcricao,
            'resumo': summary
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro na atualização: {str(e)}'}), 500

@transcricao_bp.route('/export', methods=['POST'])
def export_transcription():
    """Endpoint para exportar transcrição em formato texto"""
    try:
        data = request.get_json()
        transcricao = data.get('transcricao', [])
        resumo = data.get('resumo', {})
        
        # Gerar texto formatado
        output = []
        output.append("# TRANSCRIÇÃO DA REUNIÃO")
        output.append(f"\nData: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        output.append(f"Duração: {resumo.get('duracao_total', 0):.1f} minutos")
        output.append(f"Participantes: {resumo.get('total_falantes', 0)} pessoas")
        
        output.append("\n## TRANSCRIÇÃO COMPLETA\n")
        
        current_speaker = None
        for item in transcricao:
            if item['speaker_id'] != current_speaker:
                current_speaker = item['speaker_id']
                output.append(f"\n**{current_speaker}:**")
            
            timestamp = f"[{int(item['start']//60):02d}:{int(item['start']%60):02d}]"
            output.append(f"{timestamp} {item['text']}")
        
        output.append("\n## RESUMO DOS PONTOS PRINCIPAIS\n")
        for i, ponto in enumerate(resumo.get('pontos_principais', []), 1):
            output.append(f"{i}. {ponto}")
        
        return jsonify({
            'success': True,
            'texto_formatado': '\n'.join(output)
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro na exportação: {str(e)}'}), 500

