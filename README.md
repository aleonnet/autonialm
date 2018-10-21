# AutoNIALM

Master's Thesis Source Code - Automated Data Analytics for Motifs and Discords Mining

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

See `requirements.txt` for the required Python packages.

Make sure have the HDF5 data of the [REDD](http://redd.csail.mit.edu/) or [UK-DALE](http://jack-kelly.com/data/) dataset into a data directory. For example, `data/REDD/redd.h5` or `data/UKDALE/ukdale.h5`.


## Starting the flask server
```
# make the script executable
chmod +x flask_run.sh

# run the script to start flask server
./flask_run.sh
```

## Run AutoNIALM via command line
You also can run the code through the command line interface without having to start the Flask server. 
```
# change into directory with the cli script
cd bayesian_optimization

# run the script with specified settings
python automl_hyperopt_cli.py --datapath ../data/REDD/redd.h5 --train_building 1 --train_building 1 --train_end 2011-05-14 --test_building 1 --test_start 2011-05-14 --appliance fridge --sampling_rate 120 --epochs 10 --patience 5 --metrics_to_optimize "mean_squared_error" --max_evals 10
```
## Result files
The result will be kept in `bayesian_optimization/results/`

For each run of the AutoNIALM, the code with output two json files: One for the metadata of the results (`trial-metadata-[APPLIANCE]-[DOWNSAMPLING RATE]-[METRIC TO OPTIMIZE].json`) and another file containing information for every trial (`trial-results-[APPLIANCE]-[DOWNSAMPLING RATE]-[METRIC TO OPTIMIZE].json`).

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Neural Network approaches adapted from: https://github.com/OdysseasKr/neural-disaggregator
