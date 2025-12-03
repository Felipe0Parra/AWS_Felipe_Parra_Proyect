import base64
import json
import gzip
import datetime

# --- CONFIGURACIÓN ---
# Este nombre DEBE ser igual al que pusiste en Firehose (Destination settings -> Index)
INDEX_NAME = "backend" 

def lambda_handler(event, context):
    output_records = []
    
    for record in event['records']:
        try:
            # 1. Descomprimir datos de CloudWatch
            compressed_payload = base64.b64decode(record['data'])
            uncompressed_payload = gzip.decompress(compressed_payload)
            payload = json.loads(uncompressed_payload)
            
            cleaned_logs_parts = []
            
            # 2. Iterar sobre cada log del paquete
            if 'logEvents' in payload:
                logs = payload['logEvents']
                
                for i, log_event in enumerate(logs):
                    # --- A. Preparar el Log (La "Carne") ---
                    timestamp_iso = datetime.datetime.fromtimestamp(log_event['timestamp'] / 1000.0).isoformat()
                    
                    clean_record = {
                        '@timestamp': timestamp_iso,
                        'message': log_event['message'],
                        'logGroup': payload.get('logGroup', 'unknown')
                    }
                    
                    # Extraer RequestId para trazas (opcional)
                    if "RequestId:" in log_event['message']:
                        try:
                            parts = log_event['message'].split("RequestId: ")
                            if len(parts) > 1:
                                clean_record['requestId'] = parts[1].split()[0]
                        except:
                            pass

                    json_str = json.dumps(clean_record)
                    
                    # --- B. Inyectar Cabecera (El "Pan") ---
                    # Firehose pone la cabecera automática SOLO para la primera línea.
                    # Nosotros debemos ponerla manualmente para todas las demás (i > 0).
                    if i > 0:
                        meta_header = json.dumps({"index": {"_index": INDEX_NAME}})
                        cleaned_logs_parts.append(meta_header)
                    
                    # Agregar el log
                    cleaned_logs_parts.append(json_str)
            
            # 3. Unir todo con saltos de línea y codificar
            # El resultado será: Log1 \n Header \n Log2 \n Header \n Log3...
            final_string = "\n".join(cleaned_logs_parts) + "\n"
            
            output_records.append({
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': base64.b64encode(final_string.encode('utf-8')).decode('utf-8')
            })
            
        except Exception as e:
            print(f"CRITICAL ERROR: {str(e)}")
            # Devolver como fallido para ver el error en S3 si ocurre de nuevo
            output_records.append({
                'recordId': record['recordId'],
                'result': 'ProcessingFailed',
                'data': record['data']
            })

    return {'records': output_records}
