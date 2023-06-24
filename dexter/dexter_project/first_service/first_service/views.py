from django.shortcuts import render

import logging
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
import grpc
from google.protobuf.json_format import MessageToDict


from stubs import second_service_pb2 as audio_messages
from stubs import second_service_pb2_grpc as audio_service

from pydub import AudioSegment

debug_logger = logging.getLogger('debug_logger')

class AudioWaveView(APIView):
    """Audio wave view ."""
    def get(self, request, *args, **kwargs):
        """Entry point for get call.

        It takes audio wave and send it in chunk to other microservice.

        Args:
            request ([type]): [description]

        Returns:
            True or False .
        """
        response = {
            'Success': False,
            'ExceptionString': None
        }
        
        try:
            
            audio_path = 'first_service/assignment_audio.wav'
            chunk_duration = 20  # 20 milliseconds
            audio_chunks = cut_audio_into_chunks(audio_path, chunk_duration)

            audio_bytes = []
            for chunk in audio_chunks:
                chunk_bytes = convert_audio_to_bytes(chunk)
                audio_bytes.append(chunk_bytes)
            try:
                response = grpc_call_to_process_audio_chunks(data=audio_bytes)
            except Exception as e:
                print("Exception at 49 ", e)
                # break
            return JsonResponse(data=response, status=status.HTTP_200_OK)
        except Exception as err:
            debug_logger.exception(
                f"error in parsing data, {err}")
            response['ExceptionString'] = err.args[0]
            debug_logger.debug(
                f'log from grpc_call_to_process_audio_chunks response::{response}')
            return JsonResponse(data=response, status=status.HTTP_400_BAD_REQUEST)
        


def grpc_call_to_process_audio_chunks(data):
    """grpc_call_to_process_audio_chunks. """

    try:
        debug_logger.debug(
            f'grpc_call_to_process_audio_chunks ')
        with grpc.insecure_channel('10.9.1.2:50059') as audio_channel:
            stub = audio_service.AudioStub(
                audio_channel)
            try:
                response = stub.GetAudioChunkValue(
                    audio_messages.GetAudioChunkRequest(data=data))
            except Exception as e:
                print("Exception at grpc_call_to_process_audio_chunks ", e )
        response = MessageToDict(response, including_default_value_fields=True,
                                 preserving_proto_field_name=True)
        debug_logger.debug(f'response {response}')
        audio_channel.close()
        return response
    except Exception as e:
        debug_logger.exception(
            f"Exception in grpc_call_to_process_audio_chunks {str(e)}")
        


def cut_audio_into_chunks(audio_path, chunk_duration):
    print(" here ")
    try:
        audio = AudioSegment.from_file(audio_path)
        chunk_size = int(chunk_duration)  
        chunks = []
    
    except Exception as e:
        print("Exception at cut audio chunks ", e)
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i+chunk_size]
        chunks.append(chunk)

    return chunks

def convert_audio_to_bytes(audio):
    target_sample_rate = 16000
    audio = audio.set_frame_rate(target_sample_rate)

    audio_bytes = audio.raw_data

    return audio_bytes

