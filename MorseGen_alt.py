#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Morse Code Generator
# Author: Barry Duggan
# Description: Morse code generator
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget
import epy_block_0_0

from gnuradio import qtgui

class MorseGen_alt(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Morse Code Generator")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Morse Code Generator")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "MorseGen_alt")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.speed = speed = 12
        self.repeat = repeat = 1200
        self.baud = baud = speed/1.2
        self.volume = volume = 0.05
        self.samp_rate = samp_rate = baud*repeat
        self.freq = freq = 800

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(0, 1.0, 0.001, 0.05, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, 'Volume', "slider", float)
        self.top_grid_layout.addWidget(self._volume_win)
        self._freq_range = Range(300, 2000, 100, 800, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, 'freq', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_win)
        self.zeromq_pull_msg_source_0 = zeromq.pull_msg_source('tcp://127.0.0.1:50251', 100)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=(int)(48000/samp_rate),
                decimation=1,
                taps=None,
                fractional_bw=None)
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                30,
                200,
                firdes.WIN_HAMMING,
                6.76))
        self.epy_block_0_0 = epy_block_0_0.mc_sync_block()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, repeat)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(volume)
        self.audio_sink_0 = audio.sink(48000, 'hw:CARD=Generic,DEV=0', True)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, freq, 0.5, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.epy_block_0_0, 'msg_in'))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.epy_block_0_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "MorseGen_alt")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed
        self.set_baud(self.speed/1.2)

    def get_repeat(self):
        return self.repeat

    def set_repeat(self, repeat):
        self.repeat = repeat
        self.set_samp_rate(self.baud*self.repeat)
        self.blocks_repeat_0.set_interpolation(self.repeat)

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_samp_rate(self.baud*self.repeat)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0_0.set_k(self.volume)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 30, 200, firdes.WIN_HAMMING, 6.76))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.analog_sig_source_x_0_0.set_frequency(self.freq)





def main(top_block_cls=MorseGen_alt, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
