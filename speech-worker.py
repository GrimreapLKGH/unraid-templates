# SPDX-License-Identifier: GPL-3.0-or-later
"""Standalone local text-to-WAV utility. JSON lines in, base64 WAV out.

No application accounts, scripts, scoring or HTTP-server code is imported here.
Run with --model MODEL --voices VOICES [--threads 2]. Each input contains text,
speed, and speakers: a list of voice blends, each [[voice_id, weight], ...].
Multiple speakers are rendered as a chorus. Output is {wav: BASE64} or {error: ...}. With --task transcribe, input
{wav: BASE64} returns {transcript: TEXT}; choose --whisper-model and --model-dir.
"""
import argparse
import base64
import io
import json
import sys
import wave
import numpy as np
import onnxruntime as ort
from kokoro_onnx import Kokoro

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model');parser.add_argument('--voices')
    parser.add_argument('--task',choices=['speak','transcribe'],default='speak')
    parser.add_argument('--whisper-model',default='small.en');parser.add_argument('--model-dir')
    parser.add_argument('--threads',type=int,default=2)
    args=parser.parse_args()
    opts=ort.SessionOptions();opts.intra_op_num_threads=args.threads;opts.inter_op_num_threads=1
    # Reserve stdout exclusively for the JSON protocol, including during library startup.
    protocol=sys.stdout;sys.stdout=sys.stderr
    engine=Kokoro.from_session(ort.InferenceSession(args.model,sess_options=opts,providers=['CPUExecutionProvider']),args.voices) if args.task=='speak' else None
    for line in sys.stdin:
        try:
            request=json.loads(line)
            if args.task=='transcribe':
                if engine is None:
                    from faster_whisper import WhisperModel
                    engine=WhisperModel(args.whisper_model,device='cpu',compute_type='int8',cpu_threads=args.threads,num_workers=1,download_root=args.model_dir)
                audio=base64.b64decode(request['wav'],validate=True)
                with wave.open(io.BytesIO(audio)) as wav:
                    if wav.getnchannels()!=1 or wav.getsampwidth()!=2 or wav.getframerate()!=16000:raise ValueError('Expected mono 16 kHz PCM WAV')
                    samples=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype(np.float32)/32768.0
                segments,_=engine.transcribe(samples,language='en',beam_size=5,vad_filter=True,condition_on_previous_text=False)
                result={'transcript':' '.join(segment.text.strip() for segment in segments).strip()}
                protocol.write(json.dumps(result)+'\n');protocol.flush();continue
            text=request['text'];speed=float(request['speed']);speakers=request['speakers']
            if not isinstance(text,str) or not 1<=len(text)<=20000 or not .6<=speed<=1.3 or not 1<=len(speakers)<=8:raise ValueError('Invalid speech request')
            parts=[];rate=None
            for i,blend in enumerate(speakers):
                if not 1<=len(blend)<=8:raise ValueError('Invalid voice blend')
                for voice,weight in blend:
                    if not isinstance(voice,str) or not 0<=float(weight)<=1:raise ValueError('Invalid voice weight')
                style=blend[0][0] if len(blend)==1 and float(blend[0][1])==1 else sum(engine.get_voice_style(v)*float(w) for v,w in blend)
                audio,sample_rate=engine.create(text,voice=style,speed=speed,lang='en-gb')
                if rate is not None and rate!=sample_rate:raise ValueError('Incompatible audio rates')
                rate=sample_rate;parts.append((int(i*.025*rate),audio))
            output=np.zeros(max(offset+len(audio) for offset,audio in parts),dtype=np.float32)
            for offset,audio in parts:output[offset:offset+len(audio)]+=audio/len(parts)
            if len(parts)>1:
                peak=float(np.max(np.abs(output))) if len(output) else 0
                if peak>0:output*=min(1.5,.94/peak)
            buf=io.BytesIO()
            with wave.open(buf,'wb') as wav:
                wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate)
                wav.writeframes((np.clip(output,-1,1)*32767).astype('<i2').tobytes())
            result={'wav':base64.b64encode(buf.getvalue()).decode('ascii')}
        except Exception as error:
            print(type(error).__name__+': '+str(error),file=sys.stderr)
            result={'error':'Speech generation failed.'}
        protocol.write(json.dumps(result)+'\n');protocol.flush()
if __name__=='__main__':main()
