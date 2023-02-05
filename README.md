# multi_process_codes


# inspect_multi_process.py
  
  * Inspecting ASR data, in the format of wav-txt pair.
  * Inspecting data formats, ordering, wav duration, num_channels, bit_rate, sampling_rate.
  * Inspecting txt encoding, if txt-files are empty or not, and prints unique_characters.
  * Inspecting some other formats, which are necessary to be checked for validating our lab's ASR data.
  
  * Judges appropriate type of multi_processing accordingly to the structure of input data given. (inner-or-outer multi-processing)
  
  * Look through the code for more information.
  
 
# resampling_multi_process.py

  * Resampling ASR data, in the format of wav-txt pair.
  * Simply resamples wav datas, accordingly to the sampling_rate given by "-sr option"  (ex) -sr 8000
  * Simply copies txt datas, because this code just changes audio files.
  
  * You can multi-process by giving "-nj option" (ex) -nj 10
  
  * Look through the code for more information.
