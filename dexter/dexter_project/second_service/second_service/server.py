import grpc
from stubs import second_service_pb2 as audio_messages
from stubs import second_service_pb2_grpc as audio_service
# import webrtcvad
import numpy as np
from google.protobuf.json_format import MessageToDict


class AudioServicer(audio_service.AudioServicer):

    def GetAudioChunkValue(self, request_iterator, context):
        """Server function for second microservice which will process chunks and print if speech has ended or not """
        speech_has_finished = False
        count = 0
        try:
            req = MessageToDict(request_iterator,
                              preserving_proto_field_name=True,
                                    including_default_value_fields=False)
            req_data = req['data']
            
            length = len(req_data)
            subarrays = []
            sec = 0
            for i in range(0, length, 25):
                subarray = request_iterator.data[i:i+25]
                print("subaray len ", len(subarray))
                combined_array = self.combine_bytearrays(subarray)
                # subarrays.append(subarray)
                # break
                sample_rate = 16000  
                num_frames = len(combined_array)  
                duration = num_frames / sample_rate
                sec=sec+duration
                if sec > 3:
                    sound = self.detect_sound(combined_array)

                    if sound:
                        count = 0
                        print("Speech is ongoing")
                    else:
                        count+=1

                if count >=3:
                    speech_has_finished = True
                    print(" speech has ended ")
                    break
                    
                if sec < 50:
                    continue
                else:
                    speech_has_finished = True
                    print(" speech has ended ")
                    break
                    
        except Exception as e:
            print("exception here ", e)
        return audio_messages.GetAudioChunkResponse(Success=True)
    
    
    def detect_sound(self, byte_array):
        """ detech if byte arrays has sound or not"""
        
        audio_data = np.frombuffer(byte_array, dtype=np.int16)

        # Calculate the energy of the audio frames
        frame_size = 1024
        frames = len(audio_data) // frame_size
        energy = np.sum(np.square(audio_data[:frames * frame_size].reshape(frames, frame_size)), axis=1)

        # Set a threshold for sound detection
        energy_threshold = 50000

        # Count the number of frames with energy above the threshold
        sound_frames = np.sum(energy > energy_threshold)

        # Determine if sound is present based on the number of sound frames
        if sound_frames > 0:
            return True
        else:
            return False

    
    def combine_bytearrays(self, bytearrays):
        target_length = 500  
        chunk_length = 20  
        bytes_per_millisecond = len(bytearrays[0]) // chunk_length
        target_bytes = target_length * bytes_per_millisecond
        combined = bytearray()
        total_bytes = 0
        for ba in bytearrays:
            if total_bytes >= target_bytes:
                break

            if total_bytes + len(ba) <= target_bytes:
                combined.extend(ba)
                total_bytes += len(ba)
            else:
                remaining_bytes = target_bytes - total_bytes
                combined.extend(ba[:remaining_bytes])
                total_bytes = target_bytes
        return combined


def grpc_hook(server):
    """grpc_hook.

    Args:
        server ([type]): [description]
    """
    audio_service.add_AudioServicer_to_server(AudioServicer(), server)