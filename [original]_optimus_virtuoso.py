# -*- coding: utf-8 -*-
"""[ORIGINAL] Optimus_VIRTUOSO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zmDdAw4thW3raj3thoV_IbvKGrrcmELI

# Optimus VIRTUOSO (ver. 3.0)

## "Music never allows falsehoods for even the deaf hear flat notes!" ---OV

***

Powered by tegridy-tools TMIDI Optimus Processors with special Char Token text encoding: https://github.com/asigalov61/tegridy-tools

***

Credit for char-based GPT2 implementation used in this colab goes out to Andrej Karpathy: https://github.com/karpathy/minGPT

***

WARNING: This complete implementation is a functioning model of the Artificial Intelligence. Please excercise great humility, care, and respect. https://www.nscai.gov/

***

#### Project Los Angeles

#### Tegridy Code 2021

***

# Setup Environment, clone needed repos, and install all required dependencies
"""

#@title nvidia-smi gpu check
!nvidia-smi

#@title Install all dependencies (run only once per session)

!git clone https://github.com/asigalov61/tegridy-tools

!pip install torch
!pip install tqdm

#@title Import all needed modules

print('Loading needed modules. Please wait...')
import os

if not os.path.exists('/content/Dataset'):
    os.makedirs('/content/Dataset')

os.chdir('/content/tegridy-tools/tegridy-tools')
import TMIDI

os.chdir('/content/tegridy-tools/tegridy-tools')
from minGPT import *

from IPython.display import display, Javascript, HTML, Audio

import tqdm
from tqdm import auto

from google.colab import output, drive

os.chdir('/content/')
print('Loading complete. Enjoy! :)')

"""# Download and process MIDI dataset"""

# Commented out IPython magic to ensure Python compatibility.
#@title Download special Tegridy Piano MIDI dataset (Recommended)

#@markdown Works best stand-alone/as-is for the optimal results
# %cd /content/Dataset/

!wget 'https://github.com/asigalov61/Tegridy-MIDI-Dataset/raw/master/Tegridy-Piano-CC-BY-NC-SA.zip'
!unzip -j '/content/Dataset/Tegridy-Piano-CC-BY-NC-SA.zip'
!rm '/content/Dataset/Tegridy-Piano-CC-BY-NC-SA.zip'

# %cd /content/

# Commented out IPython magic to ensure Python compatibility.
#@title Download special Tegridy Piano Violin MIDI dataset

#@markdown Works best stand-alone/as-is for the optimal results
# %cd /content/Dataset/

!wget 'https://github.com/asigalov61/Tegridy-MIDI-Dataset/raw/master/Tegridy-Piano-Violin-CC-BY-NC-SA.zip'
!unzip -j '/content/Dataset/Tegridy-Piano-Violin-CC-BY-NC-SA.zip'
!rm '/content/Dataset/Tegridy-Piano-Violin-CC-BY-NC-SA.zip'

# %cd /content/

"""# If you are not sure where to start or what settings to select, please use original defaults"""

#@title Process MIDIs to special MIDI dataset with Tegridy MIDI Processor
#@markdown NOTES:

#@markdown 1) Dataset MIDI file names are used as song names. Feel free to change it to anything you like.

#@markdown 2) Best results are achieved with the single-track, single-channel, single-instrument MIDI 0 files with plain English names (avoid special or sys/foreign chars)

#@markdown 3) MIDI Channel = -1 means all MIDI channels except drums. MIDI Channel = 16 means all channels will be processed. Otherwise, only single indicated MIDI channel will be processed.

desired_dataset_name = "Optimus-VIRTUOSO-Music-Dataset" #@param {type:"string"}
file_name_to_output_dataset_to = "/content/Optimus-VIRTUOSO-Music-Dataset" #@param {type:"string"}
desired_MIDI_channel_to_process = 0 #@param {type:"slider", min:-1, max:16, step:1}
encode_velocities = False #@param {type:"boolean"}
encode_MIDI_channels = False #@param {type:"boolean"}
add_transposed_dataset_by_this_many_pitches = 0 #@param {type:"slider", min:-12, max:12, step:1}
add_transposed_and_flipped_dataset = False #@param {type:"boolean"}
chordify_input_MIDIs = False #@param {type:"boolean"}
melody_conditioned_chords = False #@param {type:"boolean"}
melody_pitch_baseline = 60 #@param {type:"slider", min:0, max:127, step:1}
time_denominator = 1 #@param {type:"slider", min:1, max:50, step:1}
chars_encoding_offset =  33#@param {type:"number"}

print('TMIDI Optimus MIDI Processor')
print('Starting up...')
###########

average_note_pitch = 0
min_note = 127
max_note = 0

files_count = 0

ev = 0

chords_list_f = []
melody_list_f = []

chords_list = []
chords_count = 0

melody_chords = []
melody_count = 0

TXT_String = 'DATASET=Optimus-VIRTUOSO-Music-Dataset' + chr(10)

TXT = ''
melody = []
chords = []

###########

print('Loading MIDI files...')
print('This may take a while on a large dataset in particular.')

dataset_addr = "/content/Dataset/"
os.chdir(dataset_addr)
filez = list()
for (dirpath, dirnames, filenames) in os.walk(dataset_addr):
    filez += [os.path.join(dirpath, file) for file in filenames]

# Stamping the dataset info
print('Stamping the dataset info...')

TXT_String = 'DATASET=' + str(desired_dataset_name) + chr(10)
TXT_String += 'CHARS_ENCODING_OFFSET=' + str(chars_encoding_offset) + chr(10)
TXT_String += 'TIME_DENOMINATOR=' + str(time_denominator) + chr(10)

TXT_String += 'LEGEND=STA-DUR-PTC'
if encode_velocities:
  TXT_String += '-VEL'
if encode_MIDI_channels:
  TXT_String += '-CHA'
TXT_String += chr(10)

print('Processing MIDI files. Please wait...')
for f in tqdm.auto.tqdm(filez):
  try:
    fn = os.path.basename(f)
    fn1 = fn.split('.')[0]

    files_count += 1
    TXT, melody, chords = TMIDI.Optimus_MIDI_TXT_Processor(f, chordify_TXT=chordify_input_MIDIs, output_MIDI_channels=encode_MIDI_channels, char_offset=chars_encoding_offset, dataset_MIDI_events_time_denominator=time_denominator, output_velocity=encode_velocities, MIDI_channel=desired_MIDI_channel_to_process, MIDI_patch=range(0, 127), melody_conditioned_encoding=melody_conditioned_chords, melody_pitch_baseline=melody_pitch_baseline)
    TXT_String += TXT
    melody_list_f += melody
    chords_list_f += chords

    if add_transposed_dataset_by_this_many_pitches != 0:

      TXT, melody, chords = TMIDI.Optimus_MIDI_TXT_Processor(f, chordify_TXT=chordify_input_MIDIs, output_MIDI_channels=encode_MIDI_channels, char_offset=chars_encoding_offset, dataset_MIDI_events_time_denominator=time_denominator, output_velocity=encode_velocities, MIDI_channel=desired_MIDI_channel_to_process, transpose_by=add_transposed_dataset_by_this_many_pitches, MIDI_patch=range(0, 127), melody_conditioned_encoding=melody_conditioned_chords, melody_pitch_baseline=melody_pitch_baseline)
      TXT_String += TXT
      melody_list_f += melody
      chords_list_f += chords

    if add_transposed_and_flipped_dataset == True:

      TXT, melody, chords = TMIDI.Optimus_MIDI_TXT_Processor(f, chordify_TXT=chordify_input_MIDIs, output_MIDI_channels=encode_MIDI_channels, char_offset=chars_encoding_offset, dataset_MIDI_events_time_denominator=time_denominator, output_velocity=encode_velocities, MIDI_channel=desired_MIDI_channel_to_process, transpose_by=-12, MIDI_patch=range(0, 127), flip=True, melody_conditioned_encoding=melody_conditioned_chords, melody_pitch_baseline=melody_pitch_baseline)
      TXT_String += TXT
      melody_list_f += melody
      chords_list_f += chords

  except KeyboardInterrupt:
    print('Saving current progress and quitting...')
    break  
  
  except:
    print('Bad MIDI:', f)
    continue

print('Task complete :)')
print('==================================================')
if add_transposed_dataset_by_this_many_pitches != 0:
  print('NOTE: Transposed dataset was added per users request.')
  print('==================================================')
if add_transposed_and_flipped_dataset == True:
  print('NOTE: Flipped dataset was added per users request.')  
  print('==================================================')
print('Number of processed dataset MIDI files:', files_count)
print('Number of MIDI chords recorded:', len(chords_list_f))
print('First chord event:', chords_list_f[0], 'Last chord event:', chords_list_f[-1]) 
print('Number of recorded melody events:', len(melody_list_f))
print('First melody event:', melody_list_f[0], 'Last Melody event:', melody_list_f[-1])
print('Total number of MIDI events recorded:', len(chords_list_f) + len(melody_list_f))
print('==================================================')

# Writing dataset to TXT file
with open(file_name_to_output_dataset_to + '.txt', 'wb') as f:
  f.write(TXT_String.encode('utf-8', 'replace'))
  f.close

# Dataset
MusicDataset = [chords_list_f, melody_list_f]

# Writing dataset to pickle file
TMIDI.Tegridy_Pickle_File_Writer(MusicDataset, file_name_to_output_dataset_to)

#@title Create a 3D Scatter-plot of the processed dataset

chords_flat = []
st = []
du = []
pt = []

for c in chords_list_f:
  if c[1] < 2000 and c[2] < 2000:
    st.append(c[1])
    du.append(c[2])
    pt.append(c[4])

# Creating dataset
x1 = np.array(st)
y1 = np.array(du)
z1 = np.array(pt)

#z = np.random.randint(100, size =(50))
#x = np.random.randint(80, size =(50))
#y = np.random.randint(60, size =(50))
 
# Creating figure
fig = plt.figure(figsize = (15,12))
ax = plt.axes(projection ="3d")
 
# Creating plot
ax.scatter3D(x1, y1, z1, s = 10, c = z1)
#ax.set_position()
ax.set_xlabel('Start Times')
ax.set_ylabel('Durations')
ax.set_zlabel('Pitches')
plt.title(str(desired_dataset_name))
ax.view_init(60, 30)
# show plot
plt.show()

"""# Setup and Intialize the Model

## YOU MUST RUN THE CELL/CODE IN THE SECTION BELOW to init the model. Does not matter if the model is empty or pre-trained.

## DO NOT EXECUTE TRAIN CELL/CODE UNLESS YOU INTEND TO TRAIN FROM SCRATCH
"""

#@title Create/prepare GPT2 model and load the dataset

full_path_to_training_text_file = "/content/Optimus-VIRTUOSO-Music-Dataset.txt" #@param {type:"string"}
model_attention_span_in_tokens = 512 #@param {type:"slider", min:0, max:1024, step:16}
model_embed_size = 512 #@param {type:"slider", min:0, max:1024, step:16}
number_of_heads = 8 #@param {type:"slider", min:1, max:16, step:1}
number_of_layers = 6 #@param {type:"slider", min:1, max:16, step:1}
number_of_training_epochs = 5 #@param {type:"slider", min:1, max:5, step:1}
training_batch_size = 12 #@param {type:"slider", min:4, max:256, step:4}
number_of_dataloader_threads = 4 #@param {type:"slider", min:1, max:64, step:1}
model_learning_rate = 6e-4 #@param {type:"number"}
checkpoint_full_path = "" #@param {type:"string"}

if checkpoint_full_path == '':
  checkpoint_full_path = None


trainer, model, train_dataset = MainLoader(full_path_to_training_text_file,
                                          None,
                                          number_of_dataloader_threads,
                                          model_attention_span_in_tokens,
                                          model_embed_size,
                                          number_of_heads,
                                          number_of_layers,
                                          number_of_training_epochs,
                                          training_batch_size,
                                          model_learning_rate,
                                          ckpt_path=checkpoint_full_path)

"""# Train the model or Load/Re-load the existing pre-trained model checkpoint"""

# Commented out IPython magic to ensure Python compatibility.
#@title (OPTION 1) Train the model
# %cd /content/
trainer.train()

#@title Plot Positional Embeddings

# visualize some of the learned positional embeddings, maybe they contain structure
PlotPositionalEmbeddings(model, model_attention_span_in_tokens)

# Commented out IPython magic to ensure Python compatibility.
#@title Save/Re-Save the model from memory
#@markdown Standard PyTorch AI models file extension is PTH
full_path_to_save_model_to = "/content/Optimus-VIRTUOSO-Trained-Model.pth" #@param {type:"string"}
# %cd /content/
torch.save(model, full_path_to_save_model_to)
torch.save(model.state_dict(), full_path_to_save_model_to + '.checkpoint')

#@title (OPTION 2) Load existing model/checkpoint
full_path_to_model_checkpoint = "/content/Optimus-VIRTUOSO-Trained-Model.pth" #@param {type:"string"}
model = torch.load(full_path_to_model_checkpoint)
model.eval()

"""# Generate, download, plot, and listen to the output"""

#@title Generate and download the composition as TXT file.
#@markdown PLEASE NOTE IMPORTANT POINTS: 

#@markdown 0) If you are not sure where to start/what settings to set, please use original defaults.

#@markdown 1) Model primes from the dataset !!!

#@markdown 2) Model's first output may be empty or garbled so please try several times before discarting the model

#@markdown 3) You can now communicate to the model desired length of the output composition by suffixing input_prompt with number of notes.

#@markdown I.e. SONG=Relax_with_900_notes

#@markdown 3) Coherence of GPT2 Models is inversly proportional to the length of the generated composition, so the best results are achieved with shorter compositions and/or continuation routines use

print('Optimus VIRTUOSO Model Generator')
print('Starting up...')
number_of_tokens_to_generate = 2048 #@param {type:"slider", min:0, max:32768, step:128}
creativity_temperature = 0.8 #@param {type:"slider", min:0.05, max:4, step:0.05}
top_k_prob = 64 #@param {type:"slider", min:0, max:128, step:1}
input_prompt = "SONG=" #@param {type:"string"}

os.chdir('/content/')

completion = Generate(model,
                      train_dataset,
                      trainer,
                      number_of_tokens_to_generate,
                      creativity_temperature,
                      top_k_prob,
                      input_prompt)

# Stuff for datetime stamp
filename = '/content/Optimus-VIRTUOSO-Composition-' + 'generated-on-' 
fname = TMIDI.Tegridy_File_Time_Stamp(filename)

print('Done!')
print('Saving to', str(fname + '.txt'))
with open(fname + '.txt', "w") as text_file:
    print(completion, file=text_file)

print('Downloading TXT file...')
from google.colab import files
files.download(fname + '.txt')

#@title Convert to MIDI from TXT (w/Tegridy MIDI-TXT Processor)

#@markdown Standard MIDI timings are 400/120(80)

#@markdown Please note that only the first generated composition is being converted to MIDI by default. Please check the output TXT file for extra generated compositions.
number_of_ticks_per_quarter = 400 #@param {type:"slider", min:10, max:500, step:10}
dataset_time_denominator = 1 #@param {type:"slider", min:1, max:20, step:1}
melody_conditioned_encoding = False
encoding_has_MIDI_channels = False #@param {type:"boolean"}
encoding_has_velocities = False #@param {type:"boolean"}
simulate_velocity = True #@param {type:"boolean"}
save_only_first_composition = False #@param {type:"boolean"}
chars_encoding_offset_used_for_dataset = 33 #@param {type:"number"}

print('Converting TXT to MIDI. Please wait...')

'''For debug:'''
# fname = '/content/Optimus-VIRTUOSO-Music-Dataset'

with open(fname + '.txt', 'r') as f:
  completion = f.read()

output_list, song_name = TMIDI.Tegridy_Optimus_TXT_to_Notes_Converter(completion, 
                                                                has_MIDI_channels=encoding_has_MIDI_channels, 
                                                                simulate_velocity=simulate_velocity,
                                                                char_encoding_offset=chars_encoding_offset_used_for_dataset,
                                                                save_only_first_composition=save_only_first_composition,
                                                                dataset_MIDI_events_time_denominator=dataset_time_denominator,
                                                                has_velocities=encoding_has_velocities
                                                                )

print('Converting Song to MIDI...')

output_signature = 'Optimus VIRTUOSO'

detailed_stats = TMIDI.Tegridy_SONG_to_MIDI_Converter(output_list,
                                                      output_signature = output_signature,  
                                                      output_file_name = fname, 
                                                      track_name=song_name, 
                                                      number_of_ticks_per_quarter=number_of_ticks_per_quarter)

print('Done!')

print('Downloading your composition now...')
from google.colab import files
files.download(fname + '.mid')

print('Detailed MIDI stats:')
detailed_stats

"""# Listen"""

#@title Install prereq. and import MIDI player modules (run only once)
!apt install fluidsynth #Pip does not work for some reason. Only apt works
!pip install midi2audio

from midi2audio import FluidSynth

#@title Listen to the last generated composition
#@markdown NOTE: May be very slow with the long compositions
print('Synthesizing the last output MIDI. Please stand-by... ')
FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
Audio(str(fname + '.wav'), rate=16000)

"""## Congrats! :) You did it :)"""