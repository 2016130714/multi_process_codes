'''
Sangjoon Kim
23.02.04

resampling, with multi-processing
get argparse.arguments like following

#########################  argparse.arguments list  ###################################
    1. -sr : output sampling rate you want to set.
        For example, if you want: "AAA" to be "AAA_sr8000"
        you can give "-sr 8000" option. (input sr doesn't matter)

    2. -nj : the number of jobs for multi-processing
        If you want to multi-process by 10 jobs, you can give "-nj 10" option.

    3. -i : input directories. 
        If you want to downsample "/home/AAA" to
         "/home/AAA_sr8000"
        you can give -i /home/AAA option.
    
    4. -o : output directories.
        If you want to downsample "/home/AAA" to
        "/home/AAA_sr8000"
        you can give -o /home/AAA_sr8000 option.

################ PLZ ALWAYS CHECK IF OUTPUT DIRECTORY IS EMPTY OR NOT!#############


# for a test, you can give it a try the following code
python resampling_multi_process.py -i /home/AAA -o /home/RAK_test_sr8000 -sr 8000 -nj 10
# PLZ ALWAYS CHECK IF OUTPUT DIRECTORY IS EMPTY OR NOT!

'''

import os
import re
import time
import wave
import glob
import pprint
import argparse
import subprocess
import numpy as np
from multiprocessing import Pool


class resampling_data():
    def __init__(self):

        print(f"#######################  RESAMPLING STARTED  #########################\nCurrent Time: [{time.strftime('%Y-%m-%d %H:%M:%S')}]")
        self.start_time = time.time()

##################### get argparse.arguments ##############################################################  
        parser = argparse.ArgumentParser()
        parser.add_argument('-sr', '--sample_rate', type=int,
                            required=True, help='sampling rate for inspection (necessary)')
        parser.add_argument('-nj', '--num_job', type=int,
                            help='number of jobs. If not given, inspection will be done with a single-process')
        parser.add_argument('-i', '--input_dir',
                            required=True, help='path for inspection (necessary)')
        parser.add_argument('-o', '--output_dir',
                            required=True, help='path for inspection (necessary)')
        parser.add_argument('-q', '--quiet', 
                            help="if you want quiet inspection.", action="store_false")
        self.args = parser.parse_args()

##################### variables given by arguments #############################################        
        self.input_dir = self.args.input_dir
        self.output_dir = self.args.output_dir                     
        self.sr = self.args.sample_rate
        if self.args.num_job:
            self.num_job = self.args.num_job
        else:
            self.num_job=1                                    
################################################################################################
        
        self.channel = 1
        self.bit = 16
        self.cur_dur = float()

        self.wav_list = glob.glob(self.input_dir+'/**/*.wav')
        self.wav_list.sort()
        # self.txt_list = glob.glob(self.input_dir+'/**/*.txt')
        self.readme = glob.glob(self.input_dir+'/*.md')

        self.len_wav_list = len(self.wav_list)
    
    # get split points for multi-process.
    def get_split_points(self, process_size):
        return [[process_size*i, 'to_the_end'] if i+1 == self.num_job else [process_size*i, process_size*(i+1)] for i in range(self.num_job)]


    def main(self, start_point, end_point):


        # split self.outers for multi-processing
        if end_point == 'to_the_end':
            cur_wav_list = self.wav_list[start_point:]

        else:
            cur_wav_list = self.wav_list[start_point:end_point]

        skipped_cnt=0
        for cur_wav in cur_wav_list:
            orig_txt = re.sub('\.wav$', '.txt', cur_wav)
            orig_wav = cur_wav
            cur_wav = re.sub(self.input_dir, self.output_dir+'/', cur_wav)
            cur_txt = re.sub('\.wav$', '.txt', cur_wav)
            cur_dir = re.sub('[^/]+\.wav$', '', cur_wav)
            
            # make directories
            os.makedirs(cur_dir, exist_ok=True)

            # resample waves
            sox_cmd = f"sox {orig_wav} -r {self.sr} -c {self.channel} -b {self.bit} {cur_wav}"
            os.system(sox_cmd)


            cp_cmd = f"cp {orig_txt} {cur_txt}"
            os.system(cp_cmd)

        print(f"resampling of {cur_dir} is done.")


        return None

    

    def multi_process_main(self):
        total_dur=float()
        total_uniq_chars=set()
        total_extra_infos=set()
        process_size = int(self.len_wav_list / self.num_job)
        split_points = self.get_split_points(process_size)


        with Pool(self.num_job) as p:

            try:
                # multi-process 핵심: self.main([100,200]) 이런 식으로 인자값 전달. (2개 이상의 인자를 전달하기 위해 starmap 사용)
                all_results = p.starmap(self.main, split_points)
                p.close()
                p.join()
            # In case parent process is intentionally killed by KeyboardInterrupt, kill all the lasting children processes.
            except:
                p.terminate()
        
        # copy readme
        for readme in self.readme:
            save_readme = re.sub(self.input_dir, self.output_dir+'/', readme)
            cp_cmd = f"cp {readme} {save_readme}"

            os.system(cp_cmd)
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        print("\nAll the files are resampled. Resampling is terminated")
        print("\nSpent time: %dhr %02dmin %02dsec" % (elapsed_time // 3600, (elapsed_time % 3600 // 60), (elapsed_time % 60)))
        print(f"#######################  RESAMPLING TERMINATED  #########################\nCurrent Time: [{time.strftime('%Y-%m-%d %H:%M:%S')}]")

        return None


if __name__ == '__main__':

    inspect = resampling_data()
    inspect.multi_process_main()
