#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Uplink decoding demo
# Author: Piotr Krysik
# Description: Demonstration of uplink decoding using data captured with use of Multi-rtl
# Generated: Mon May 23 16:48:53 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import grgsm
import pmt


class uplink_decoding_multi_rtl(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Uplink decoding demo")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6

        ##################################################
        # Blocks
        ##################################################
        self.gsm_sdcch8_demapper_0 = grgsm.gsm_sdcch8_demapper(
            timeslot_nr=1,
        )
        self.gsm_receiver_with_uplink_0 = grgsm.receiver(4, ([0]), ([2]), True)
        self.gsm_message_printer_0_0 = grgsm.message_printer(pmt.intern(""), False,
            False, False)
        self.gsm_input_0_0 = grgsm.gsm_input(
            ppm=0,
            osr=4,
            fc=947.8e6-45e6,
            samp_rate_in=samp_rate,
        )
        self.gsm_input_0 = grgsm.gsm_input(
            ppm=0,
            osr=4,
            fc=947.8e6,
            samp_rate_in=samp_rate,
        )
        self.gsm_decryption_0_3 = grgsm.decryption(([0x46,0x77,0x2d,0x54,0xa3,0xa3,0xc3,0x1c]), 1)
        self.gsm_control_channels_decoder_0_1_0 = grgsm.control_channels_decoder()
        self.gsm_control_channels_decoder_0_1 = grgsm.control_channels_decoder()
        self.gsm_clock_offset_control_0 = grgsm.clock_offset_control(947.8e6)
        self.blocks_socket_pdu_0_0_0 = blocks.socket_pdu("UDP_CLIENT", "127.0.0.1", "4729", 10000, False)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, "sms_multirtl_uplink_tail", False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, "sms_multirtl_downlink_tail", False)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gsm_clock_offset_control_0, 'ppm'), (self.gsm_input_0, 'ppm_in'))    
        self.msg_connect((self.gsm_clock_offset_control_0, 'ppm'), (self.gsm_input_0_0, 'ppm_in'))    
        self.msg_connect((self.gsm_control_channels_decoder_0_1, 'msgs'), (self.blocks_socket_pdu_0_0_0, 'pdus'))    
        self.msg_connect((self.gsm_control_channels_decoder_0_1, 'msgs'), (self.gsm_message_printer_0_0, 'msgs'))    
        self.msg_connect((self.gsm_control_channels_decoder_0_1_0, 'msgs'), (self.blocks_socket_pdu_0_0_0, 'pdus'))    
        self.msg_connect((self.gsm_control_channels_decoder_0_1_0, 'msgs'), (self.gsm_message_printer_0_0, 'msgs'))    
        self.msg_connect((self.gsm_decryption_0_3, 'bursts'), (self.gsm_control_channels_decoder_0_1_0, 'bursts'))    
        self.msg_connect((self.gsm_receiver_with_uplink_0, 'measurements'), (self.gsm_clock_offset_control_0, 'measurements'))    
        self.msg_connect((self.gsm_receiver_with_uplink_0, 'C0'), (self.gsm_sdcch8_demapper_0, 'bursts'))    
        self.msg_connect((self.gsm_sdcch8_demapper_0, 'bursts'), (self.gsm_control_channels_decoder_0_1, 'bursts'))    
        self.msg_connect((self.gsm_sdcch8_demapper_0, 'bursts'), (self.gsm_decryption_0_3, 'bursts'))    
        self.connect((self.blocks_file_source_0, 0), (self.gsm_input_0, 0))    
        self.connect((self.blocks_file_source_0_0, 0), (self.gsm_input_0_0, 0))    
        self.connect((self.gsm_input_0, 0), (self.gsm_receiver_with_uplink_0, 0))    
        self.connect((self.gsm_input_0_0, 0), (self.gsm_receiver_with_uplink_0, 1))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.gsm_input_0.set_samp_rate_in(self.samp_rate)
        self.gsm_input_0_0.set_samp_rate_in(self.samp_rate)


def main(top_block_cls=uplink_decoding_multi_rtl, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
