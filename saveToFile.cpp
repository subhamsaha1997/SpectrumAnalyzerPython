#include <uhd/utils/thread.hpp>
#include<uhd/utils/safe_main.hpp>
#include<uhd/usrp/multi_usrp.hpp>
#include<iostream>
#include<csignal>
#include<fstream>
#include<complex>

int UHD_SAFE_MAIN(int argc, char* argv[]){
	uhd::set_thread_priority_safe();

	const std::string args = "type=b200";
	std::string file = "capture.bin";
	double freq = 4.5e9;
	double rate = 4e6;
	double gain = 30;

	double duration = 1;
	

	if (argc > 1){
		file = argv[1];
		freq = atof(argv[2]);
		rate = atof(argv[3]);
		gain = atof(argv[4]);
		duration = atof(argv[5]);

	}
	const int samps_total = int(rate*duration);
	printf("Number of samples to be written: %d",samps_total);

	const size_t samps_per_buff = samps_total;
	const size_t samps_per_loop = 16000;

	uhd::usrp::multi_usrp::sptr usrp = uhd::usrp::multi_usrp::make(args);
	usrp->set_rx_rate(rate);
	usrp->set_rx_freq(freq);
	usrp->set_rx_gain(gain);

	uhd::stream_args_t stream_args(std::string("fc64"));
	uhd::rx_streamer::sptr rx_stream = usrp->get_rx_stream(stream_args);

	uhd::rx_metadata_t metadata;
	std::vector<std::complex<double>> buff(samps_per_buff);

	std::ofstream outfile((file.c_str()), std::ofstream::binary);

	size_t rx_total = 0;
	size_t i = 0;
	printf("Starting to record!\n");

	uhd::stream_cmd_t stream_cmd(uhd::stream_cmd_t::STREAM_MODE_NUM_SAMPS_AND_DONE);

	stream_cmd.num_samps = samps_total;
	stream_cmd.stream_now = true;
	usrp->issue_stream_cmd(stream_cmd);



	while (rx_total < samps_total){
		while(i < samps_per_buff){
			size_t rx_num_samps = rx_stream-> recv(&buff.at(i),samps_per_loop,metadata);
			i += rx_num_samps;

			std::cout <<".";
			flush(std::cout);

			if (metadata.error_code == uhd::rx_metadata_t::ERROR_CODE_OVERFLOW){
				printf("o");
			}
			else if(metadata.error_code != uhd::rx_metadata_t::ERROR_CODE_NONE){
				printf("*");
			}
		}

		outfile.write((const char*) & buff.front(), i*sizeof(std::complex<double>));

		rx_total += i;

		i = 0;

	}

	outfile.close();
	printf("\n\n Done!\n");
	return 0;



}
