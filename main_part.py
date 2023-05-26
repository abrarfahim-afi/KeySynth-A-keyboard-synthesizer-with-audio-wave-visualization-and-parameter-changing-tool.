# Main 14/12/2021
# Additional files: Load_File.py , string_counter.py, counter.txt

import pyaudio, struct
import numpy as np
from scipy import signal
import scipy.io.wavfile as wavfile
from math import asin,sin, cos, pi
import tkinter as Tk     
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import wave
from Load_File import SPECTROGRAM
from string_counter import previous_counter, update_counter


# Pyaudio parameters
BLOCKLEN   = 512*2      # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second





# Parameter for clipping
MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)
    
# Creating a Tkinter widget for choosing type of piano input

root1 = Tk.Tk()

S1 = Tk.StringVar()
S1.set('Keysynth Input Selection')


# Defining a Label 
L1 = Tk.Label(root1,  textvariable= S1)

# Defining the buttons
def piano_selection_button():
    #while True:
        #root1.update()
        global button_input
        choice  = var.get()
        if choice == 1:
            output = "Sine"
            button_input = 0
            #print(button_input)
            #messagebox.showinfo('Keysynth Input Selection', 'You Selected {output}.',root1.quit())
        
        elif choice == 2:
            output =  "Sawtooth"
            button_input = 1
            #print(button_input)
            #messagebox.showinfo('Keysynth Input Selection', 'You Selected {output}.',root1.quit())
        
        elif choice == 3:
            output =  "Triangle"
            button_input = 2
            #print(button_input)
            #messagebox.showinfo('Keysynth Input Selection', 'You Selected {output}.',root1.quit())
        
        elif choice == 4:
            output =  "Load Spectrogram of previous file"
            # Open wave file
            fileStatus = SPECTROGRAM()
            if fileStatus == False:
                messagebox.showinfo('ERROR: NO SAVED FILE', 'There is no previous composition. Kindly built another one.',root1.quit())
    
        else:
            output = "Invalid selection"

        #return messagebox.showinfo('Keysynth Input Selection', 'You Selected {output}.',root1.quit())
        root1.quit()
        #return button_input
        
        
def callback_quit():
    print("Good Bye")
    root1.quit()
 
var = Tk.IntVar()
B1 = Tk.Radiobutton(root1, text="Sine", variable=var, value=1, command=piano_selection_button)
B2 = Tk.Radiobutton(root1, text="Sawtooth", variable=var, value=2, command=piano_selection_button)
B3 = Tk.Radiobutton(root1, text="Triangle", variable=var, value=3, command=piano_selection_button)
B4 = Tk.Radiobutton(root1, text="Load Saved Audio Spectrogram", variable=var, value=4, command=piano_selection_button)
B5 = Tk.Button(root1, text = "Quit", command = callback_quit)

# Placeing the buttons
L1.pack()
B1.pack(fill = Tk.X)
B2.pack(fill = Tk.X)
B3.pack(fill = Tk.X)
B4.pack(fill = Tk.X)
B5.pack(fill = Tk.X)

root1.mainloop()


next_counter_number = int(previous_counter()) + 1
output_wavefile = str(next_counter_number) + 'KeySynth_piano.wav'
wf = wave.open(output_wavefile, 'w')      # wave file
wf.setnchannels(CHANNELS)      # one channel (mono)
wf.setsampwidth(WIDTH)      # two bytes per sample
wf.setframerate(RATE)   # samples per second

# Describes the parameters such as coefficients and frequencies
def input_wave(piano_type):
    # Parameters
    
    global f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12
    global a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12
    global b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12
    
    Ta = 0.5    # Decay time (seconds) # Add a fucntion to change the decay time
    f1 = 440  # Frequency (Hz) # Add function for changing the frequency
    f2 = f1 * 2 ** (1.0/12.0)
    f3 = f1 * 2 ** (2.0/12.0)
    f4 = f1 * 2 ** (3.0/12.0)
    f5 = f1 * 2 ** (4.0/12.0)
    f6 = f1 * 2 ** (5.0/12.0)
    f7 = f1 * 2 ** (6.0/12.0)
    f8 = f1 * 2 ** (7.0/12.0)
    f9 = f1 * 2 ** (8.0/12.0)
    f10 = f1 * 2 ** (9.0/12.0)
    f11 = f1 * 2 ** (10.0/12.0)
    f12 = f1 * 2 ** (11.0/12.0)

    
    if piano_type == 0:
    
        # Pole radius and angle
        r = 0.02**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
        om1  = 2.0 * pi * float(f1)/RATE
        om2  = 2.0 * pi * float(f2)/RATE
        om3  = 2.0 * pi * float(f3)/RATE
        om4  = 2.0 * pi * float(f4)/RATE
        om5  = 2.0 * pi * float(f5)/RATE
        om6  = 2.0 * pi * float(f6)/RATE
        om7  = 2.0 * pi * float(f7)/RATE
        om8  = 2.0 * pi * float(f8)/RATE
        om9  = 2.0 * pi * float(f9)/RATE
        om10  = 2.0 * pi * float(f10)/RATE
        om11  = 2.0 * pi * float(f11)/RATE
        om12  = 2.0 * pi * float(f12)/RATE


        # Coefficients of a second order filter.
        # Here each note has 2 coefficients. Such as Note A1 has a1 and b2 coefficent 
        a1  = [1, -2*r*cos(om1), r**2]
        a2  = [1, -2*r*cos(om2), r**2]
        a3  = [1, -2*r*cos(om3), r**2]
        a4  = [1, -2*r*cos(om4), r**2]
        a5  = [1, -2*r*cos(om5), r**2]
        a6  = [1, -2*r*cos(om6), r**2]
        a7  = [1, -2*r*cos(om7), r**2]
        a8  = [1, -2*r*cos(om8), r**2]
        a9  = [1, -2*r*cos(om9), r**2]
        a10  = [1, -2*r*cos(om10), r**2]
        a11  = [1, -2*r*cos(om11), r**2]
        a12  = [1, -2*r*cos(om12), r**2]
       


        b1  = [r*sin(om1)]
        b2  = [r*sin(om2)]
        b3  = [r*sin(om3)]
        b4  = [r*sin(om4)]
        b5  = [r*sin(om5)]
        b6  = [r*sin(om6)]
        b7  = [r*sin(om7)]
        b8  = [r*sin(om8)]
        b9  = [r*sin(om9)]        
        b10  = [r*sin(om10)]
        b11  = [r*sin(om11)]
        b12  = [r*sin(om12)]
        
        
    elif piano_type == 1:
        
        def ip(om):
            return signal.sawtooth(om)
            
        # Pole radius and angle       
        r = 0.02**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
        om1  = 2.0 * pi * float(f1)/RATE
        om2  = 2.0 * pi * float(f2)/RATE
        om3  = 2.0 * pi * float(f3)/RATE
        om4  = 2.0 * pi * float(f4)/RATE
        om5  = 2.0 * pi * float(f5)/RATE
        om6  = 2.0 * pi * float(f6)/RATE
        om7  = 2.0 * pi * float(f7)/RATE
        om8  = 2.0 * pi * float(f8)/RATE
        om9  = 2.0 * pi * float(f9)/RATE
        om10  = 2.0 * pi * float(f10)/RATE
        om11  = 2.0 * pi * float(f11)/RATE
        om12  = 2.0 * pi * float(f12)/RATE
            
         # Here each note has 2 coefficients. Such as Note A1 has a1 and b2 coefficent. Filter coefficients
        a1  = [1, -2*r*ip(om1), r**2]
        a2  = [1, -2*r*ip(om2), r**2]
        a3  = [1, -2*r*ip(om3), r**2]
        a4  = [1, -2*r*ip(om4), r**2]
        a5  = [1, -2*r*ip(om5), r**2]
        a6  = [1, -2*r*ip(om6), r**2]
        a7  = [1, -2*r*ip(om7), r**2]
        a8  = [1, -2*r*ip(om8), r**2]
        a9  = [1, -2*r*ip(om9), r**2]
        a10  = [1, -2*r*ip(om10), r**2]
        a11  = [1, -2*r*ip(om11), r**2]
        a12  = [1, -2*r*ip(om12), r**2]
        
        
        b1  = [r*ip(om1)]
        b2  = [r*ip(om2)]
        b3  = [r*ip(om3)]
        b4  = [r*ip(om4)]
        b5  = [r*ip(om5)]
        b6  = [r*ip(om6)]
        b7  = [r*ip(om7)]
        b8  = [r*ip(om8)]
        b9  = [r*ip(om9)]        
        b10  = [r*ip(om10)]
        b11  = [r*ip(om11)]
        b12  = [r*ip(om12)]
    
    elif piano_type == 2:
        
        def ip(om):
            return asin(sin(om))
        
        # Pole radius and angle       
        r = 0.02**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
        om1  = 2.0 * pi * float(f1)/RATE
        om2  = 2.0 * pi * float(f2)/RATE
        om3  = 2.0 * pi * float(f3)/RATE
        om4  = 2.0 * pi * float(f4)/RATE
        om5  = 2.0 * pi * float(f5)/RATE
        om6  = 2.0 * pi * float(f6)/RATE
        om7  = 2.0 * pi * float(f7)/RATE
        om8  = 2.0 * pi * float(f8)/RATE
        om9  = 2.0 * pi * float(f9)/RATE
        om10  = 2.0 * pi * float(f10)/RATE
        om11  = 2.0 * pi * float(f11)/RATE
        om12  = 2.0 * pi * float(f12)/RATE
            
         # Here each note has 2 coefficients. Such as Note A1 has a1 and b2 coefficent 
        a1  = [1, -2*r*ip(om1), r**2]
        a2  = [1, -2*r*ip(om2), r**2]
        a3  = [1, -2*r*ip(om3), r**2]
        a4  = [1, -2*r*ip(om4), r**2]
        a5  = [1, -2*r*ip(om5), r**2]
        a6  = [1, -2*r*ip(om6), r**2]
        a7  = [1, -2*r*ip(om7), r**2]
        a8  = [1, -2*r*ip(om8), r**2]
        a9  = [1, -2*r*ip(om9), r**2]
        a10  = [1, -2*r*ip(om10), r**2]
        a11  = [1, -2*r*ip(om11), r**2]
        a12  = [1, -2*r*ip(om12), r**2]
        A = [ a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12]
        
        
        b1  = [r*ip(om1)]
        b2  = [r*ip(om2)]
        b3  = [r*ip(om3)]
        b4  = [r*ip(om4)]
        b5  = [r*ip(om5)]
        b6  = [r*ip(om6)]
        b7  = [r*ip(om7)]
        b8  = [r*ip(om8)]
        b9  = [r*ip(om9)]        
        b10  = [r*ip(om10)]
        b11  = [r*ip(om11)]
        b12  = [r*ip(om12)]
        
        
            

# Function called for Frequencies and Coefficients
piano_type = button_input
input_wave(piano_type)
      

ORDER = 2   # filter order

# States of the lfilter
states1 = np.zeros(ORDER)
states2 = np.zeros(ORDER)
states3 = np.zeros(ORDER)
states4 = np.zeros(ORDER)
states5 = np.zeros(ORDER)
states6 = np.zeros(ORDER)
states7 = np.zeros(ORDER)
states8 = np.zeros(ORDER)
states9 = np.zeros(ORDER)
states10 = np.zeros(ORDER)
states11 = np.zeros(ORDER)
states12 = np.zeros(ORDER)


x1  = np.zeros(BLOCKLEN)
x2  = np.zeros(BLOCKLEN)
x3  = np.zeros(BLOCKLEN)
x4  = np.zeros(BLOCKLEN)
x5  = np.zeros(BLOCKLEN)
x6  = np.zeros(BLOCKLEN)
x7  = np.zeros(BLOCKLEN)
x8  = np.zeros(BLOCKLEN)
x9  = np.zeros(BLOCKLEN)
x10 = np.zeros(BLOCKLEN)
x11 = np.zeros(BLOCKLEN)
x12 = np.zeros(BLOCKLEN)

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
        format      = PA_FORMAT,
        channels    = CHANNELS,
        rate        = RATE,
        input       = False,
        output      = True,
        frames_per_buffer = 32)
# specify low frames_per_buffer to reduce latency

CONTINUE   = True
KEYPRESS1  = False
KEYPRESS2  = False
KEYPRESS3  = False
KEYPRESS4  = False
KEYPRESS5  = False
KEYPRESS6  = False
KEYPRESS7  = False
KEYPRESS8  = False
KEYPRESS9  = False
KEYPRESS10 = False
KEYPRESS11 = False
KEYPRESS12 = False



def my_function(event):
                global CONTINUE
                
                global KEYPRESS1
                global KEYPRESS2
                global KEYPRESS3
                global KEYPRESS4
                global KEYPRESS5
                global KEYPRESS6
                global KEYPRESS7
                global KEYPRESS8
                global KEYPRESS9
                global KEYPRESS10
                global KEYPRESS11
                global KEYPRESS12

                print('You pressed ' + event.char)
                if event.char == 'q':
                    print('Good bye')
                    CONTINUE = False
                #KEYPRESS = True
                f1 = 440
                # Keyes to the keyboard: A,S,D,F,G,H,Z,X,C,V,B,N
                if event.char == 'a':
                    f1 = 440       # Just to show the frequency
                    print('Frequency: %.2f' %f1)
                    KEYPRESS1 = True
                
                if event.char == 's':
                    f2 = f1 * 2 ** (1.0/12.0)
                    print('Frequency: %.2f' %f2)
                    KEYPRESS2 = True
                    
                if event.char == 'd':
                    f3 = f1 * 2 ** (2.0/12.0)
                    print('Frequency: %.2f' %f3)
                    KEYPRESS3 = True
                
                if event.char == 'f':
                    f4 = f1 * 2 ** (3.0/12.0)
                    print('Frequency: %.2f' %f4)
                    KEYPRESS4 = True
                    
                if event.char == 'g':
                    f5 = f1 * 2 ** (4.0/12.0)
                    print('Frequency: %.2f' %f5)
                    KEYPRESS5 = True
                    
                if event.char == 'h':
                    f6 = f1 * 2 ** (5.0/12.0)
                    print('Frequency: %.2f' %f6)
                    KEYPRESS6 = True
                    
                if event.char == 'z':
                    f7 = f1 * 2 ** (6.0/12.0)
                    print('Frequency: %.2f' %f7)
                    KEYPRESS7 = True
                    
                if event.char == 'x':
                    f8 = f1 * 2 ** (7.0/12.0)
                    print('Frequency: %.2f' %f8)
                    KEYPRESS8 = True
                
                if event.char == 'c':
                    f9 = 440 * 2 ** (8.0/12.0)
                    print('Frequency: %.2f' %f9)
                    KEYPRESS9 = True
                    
                if event.char == 'v':
                    f10 = f1 * 2 ** (9.0/12.0)
                    print('Frequency: %.2f' %f10)
                    KEYPRESS10 = True
                    
                if event.char == 'b':
                    f11 = f1 * 2 ** (10.0/12.0)
                    print('Frequency: %.2f' %f11)
                    KEYPRESS11 = True
                    
                if event.char == 'n':
                    f12 = f1 * 2 ** (11.0/12.0)
                    print('Frequency: %.2f' %f12)
                    KEYPRESS12 = True
                    

root = Tk.Tk()
#root.config(cursor="none")   # Removes cursor from the figure.
root.bind("<Key>", my_function)
root.geometry("700x800")        # Dimension of the Tkinter window

# Define Tk variables for slider
global frequency
frequency = Tk.DoubleVar()
gain = Tk.DoubleVar()
#Transition = Tk.DoubleVar()

# Initialize Tk variables for slider
gain.set(1000)

L1 = Tk.Label(root, text = 'KeySynth', bg="purple", fg="white")
S_gain = Tk.Scale(root, label = 'Gain', bg="purple", fg="white", variable = gain,orient= Tk.HORIZONTAL, from_ = 1000, to = 20000, tickinterval =1000)
L2 = Tk.Label(root, text = 'Piano Buttons')
L3 = Tk.Label(root, text = ' A => Note A | S => Note B Flat | D => Note B | F => Note C | G => Note C sharp | H => Note D ' )
L4 = Tk.Label(root, text = ' Z => Note D sharp | X => Note E | C => Note F| V => Note F Sharp | B => Note G | N => Note A Flat ')


L1.pack(fill = Tk.X)
L2.pack()
L3.pack()
L4.pack()
S_gain.pack(side = Tk.BOTTOM, fill = Tk.X)
print('Press keys for sound.')
print('Press "q" to quit')

t = [1000.*i/RATE for i in range(BLOCKLEN)]
freq = RATE/BLOCKLEN * np.arange(0, BLOCKLEN)

pyplot.ion()           # Turn on interactive mode so plot gets updated

x = np.zeros(BLOCKLEN)
my_fig = pyplot.figure(1)
my_fig.set_size_inches(7.5, 8.5,forward=True)  # Sets figure size in inches. To propagate the size change to an existing GUI window, forward=True is used
pyplot.close()            # Closes the figure for the pyplot. But Tkinter figure remains as it is.
my_plot = my_fig.add_subplot(2, 1, 1)
[my_line] = my_plot.plot(t, x,color='RED')
#my_plot.title('Signal in Time Domain')
my_plot.set_ylim(-32000, 32000)
my_plot.set_xlim(0, BLOCKLEN*1000.0/RATE)   # Time axis in milliseconds a
my_plot.set_xlabel('Time (milliseconds)')
my_plot.set_ylabel('Amplitude')
my_plot.grid(True)

# For Frequency
my_plot_2 = my_fig.add_subplot(2, 1, 2)
[my_line2] = my_plot_2.plot(freq, x)
#my_plot.title('Signal in Frequency Domain')
my_plot_2.set_ylim(0, 32000)
my_plot_2.set_xlim(0, 4000)   # Frequency Axis in Hertz 
my_plot_2.set_xlabel('Frequency in Hertz') 
my_plot_2.set_ylabel('Amplitude')
my_plot_2.grid(True)
 

# Turn fig into a Tkinter widget
my_canvas = FigureCanvasTkAgg(my_fig, master = root)
# my_fig.canvas.draw()

W1 = my_canvas.get_tk_widget()
W1.pack()

if button_input == 0:
    M = int(BLOCKLEN/2.0)  # Change this for sawtooth. we can change M by using button input value. For button input value == 0 set M = int(BLOCKLEN/2.0) otherwise M = 0
else:
    M = 0


while CONTINUE:
    root.update()
    if KEYPRESS1 and CONTINUE:
                    x1[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f  Note A' % f1 )
                    else:
                         my_plot.set_title('Frequency')
                    
    if KEYPRESS2 and CONTINUE:
                    x2[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f Note B Flat' % f2 )
                    else:
                         my_plot.set_title('Frequency')
                
    if KEYPRESS3 and CONTINUE:
                    x3[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f Note B' % f3 )
                    else:
                         my_plot.set_title('Frequency')
                
    if KEYPRESS4 and CONTINUE:
                    x4[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f Note C' % f4 )
                    else:
                         my_plot.set_title('Frequency')
                
    if KEYPRESS5 and CONTINUE:
                    x5[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f Note C sharp' % f5 )
                    else:
                         my_plot.set_title('Frequency')
                
    if KEYPRESS6 and CONTINUE:
                    x6[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f Note D' % f6 )
                    else:
                         my_plot.set_title('Frequency')
                
    if KEYPRESS7 and CONTINUE:
                    x7[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f Note D sharp' % f7 )
                    else:
                         my_plot.set_title('Frequency')
                
    if KEYPRESS8 and CONTINUE:
                    x8[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f Note E' % f8 )
                    else:
                         my_plot.set_title('Frequency')
                
    if KEYPRESS9 and CONTINUE:
                    x9[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f Note F' % f9 )
                    else:
                         my_plot.set_title('Frequency')
                
    if KEYPRESS10 and CONTINUE:
                    x10[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f Note F Sharp' % f10 )
                    else:
                         my_plot.set_title('Frequency')
                    
    if KEYPRESS11 and CONTINUE:
                    x11[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f Note G' % f11 )
                    else:
                         my_plot.set_title('Frequency')
                    
                
    if KEYPRESS12 and CONTINUE:
                    x12[M] = S_gain.get()
                    if button_input == 0:
                        my_plot.set_title('Frequency = %.2f Note A Flat' % f12 )
                    else:
                         my_plot.set_title('Frequency')
    
   

    [y1  , states1] = signal.lfilter(b1,  a1,  x1, zi= states1)
    [y2  , states2] = signal.lfilter(b2,  a2,  x2, zi= states2)
    [y3  , states3] = signal.lfilter(b3,  a3,  x3, zi= states3)
    [y4  , states4] = signal.lfilter(b4,  a4,  x4, zi= states4)
    [y5  , states5] = signal.lfilter(b5,  a5,  x5, zi= states5)
    [y6  , states6] = signal.lfilter(b6,  a6,  x6, zi= states6)
    [y7  , states7] = signal.lfilter(b7,  a7,  x7, zi= states7)
    [y8  , states8] = signal.lfilter(b8,  a8,  x8, zi= states8)
    [y9  , states9] = signal.lfilter(b9,  a9,  x9, zi= states9)
    [y10 , states10] = signal.lfilter(b10, a10, x10, zi= states10)
    [y11 , states11] = signal.lfilter(b11, a11, x11, zi= states11)
    [y12 , states12] = signal.lfilter(b12, a12, x12, zi= states12)
    
    x1[M] = 0.0
    x2[M] = 0.0
    x3[M] = 0.0
    x4[M] = 0.0
    x5[M] = 0.0
    x6[M] = 0.0
    x7[M] = 0.0
    x8[M] = 0.0
    x9[M] = 0.0
    x10[M] = 0.0
    x11[M] = 0.0
    x12[M] = 0.0   
        
    
    KEYPRESS1 = False
    KEYPRESS2 = False
    KEYPRESS3 = False
    KEYPRESS4 = False
    KEYPRESS5 = False
    KEYPRESS6 = False
    KEYPRESS7 = False
    KEYPRESS8 = False
    KEYPRESS9 = False
    KEYPRESS10 = False
    KEYPRESS11 = False
    KEYPRESS12 = False

    ytotal = y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8 + y9 + y10 + y11 + y12
    my_line.set_ydata(ytotal)
    
    
    ytotal = np.clip(ytotal.astype(int), - MAXVALUE, MAXVALUE)    # Clipping
    
    output_block = np.fft.fft(ytotal)
    #output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)
    my_line2.set_ydata(np.abs(output_block))
    pyplot.pause(0.001)
                
    

    binary_data = struct.pack('h' * BLOCKLEN, *ytotal);    # Convert to binary binary_data
    stream.write(binary_data, BLOCKLEN) 
    # Information about saving the audio file.
    
    wf.writeframes(binary_data)  
   
    
    

print('* Done.')
pyplot.ioff()           # Turn off interactive mode

# Close audio stream
update_counter(next_counter_number)
stream.stop_stream()
stream.close()
p.terminate()
wf.close()


