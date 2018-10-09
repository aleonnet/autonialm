from __future__ import print_function, division
import warnings
warnings.filterwarnings("ignore")

import time

from nilmtk import DataSet, TimeFrame, MeterGroup, HDFDataStore
from nilmtk.disaggregate import CombinatorialOptimisation

import pandas as pd

# Bring packages onto the path
import sys, os
sys.path.append(os.path.abspath('../bayesian_optimization/'))

from utils import metrics

def combinatorial_optimisation(dataset_path, train_building, train_start, train_end, test_building, test_start, test_end, meter_key, sample_period):

    # Start tracking time
    start = time.time()

    # Prepare dataset and options
    # print("========== OPEN DATASETS ============")
    dataset_path = dataset_path
    train = DataSet(dataset_path)
    train.set_window(start=train_start, end=train_end)
    test = DataSet(dataset_path)
    test.set_window(start=test_start, end=test_end)
    train_building = train_building
    test_building = test_building
    meter_key = meter_key

    sample_period = sample_period


    train_elec = train.buildings[train_building].elec
    test_elec = test.buildings[test_building].elec

    appliances = [meter_key]
    selected_meters = [train_elec[app] for app in appliances]
    selected_meters.append(train_elec.mains())
    selected = MeterGroup(selected_meters)

    co = CombinatorialOptimisation()

    # print("========== TRAIN ============")
    co.train(selected, sample_period=sample_period)

    # print("========== DISAGGREGATE ============")
    disag_filename = 'disag-out.h5'
    output = HDFDataStore(disag_filename, 'w')
    co.disaggregate(test_elec.mains(), output_datastore=output)
    output.close()

    # print("========== RESULTS ============")
    result = DataSet(disag_filename)
    res_elec = result.buildings[test_building].elec
    rpaf = metrics.recall_precision_accuracy_f1(res_elec[meter_key], test_elec[meter_key])

    metrics_results_dict = {
        'recall_score': rpaf[0],
        'precision_score': rpaf[1],
        'accuracy_score': rpaf[2],
        'f1_score': rpaf[3],
        'mean_absolute_error': metrics.mean_absolute_error(res_elec[meter_key], test_elec[meter_key]),
        'mean_squared_error': metrics.mean_square_error(res_elec[meter_key], test_elec[meter_key]),
        'relative_error_in_total_energy': metrics.relative_error_total_energy(res_elec[meter_key], test_elec[meter_key]),
        'nad': metrics.nad(res_elec[meter_key], test_elec[meter_key]),
        'disaggregation_accuracy': metrics.disaggregation_accuracy(res_elec[meter_key], test_elec[meter_key])
        }

    # end tracking time
    end = time.time()

    time_taken = end-start # in seconds

    # model_result_data = {
    #     'algorithm_name': 'CO',
    #     'datapath': dataset_path,
    #     'train_building': train_building,
    #     'train_start': str(train_start.date()) if train_start != None else None ,
    #     'train_end': str(train_end.date()) if train_end != None else None ,
    #     'test_building': test_building,
    #     'test_start': str(test_start.date()) if test_start != None else None ,
    #     'test_end': str(test_end.date()) if test_end != None else None ,
    #     'appliance': meter_key,
    #     'sampling_rate': sample_period,
    #
    #     'algorithm_info': {
    #         'options': {
    #             'epochs': None
    #         },
    #         'hyperparameters': {
    #             'sequence_length': None,
    #             'min_sample_split': None,
    #             'num_layers': None
    #         },
    #         'profile': {
    #             'parameters': None
    #         }
    #     },
    #
    #     'metrics':  metrics_results_dict,
    #
    #     'time_taken': format(time_taken, '.2f'),
    # }

    model_result_data = {
        'metrics':  metrics_results_dict,
        'time_taken': format(time_taken, '.2f'),
        'epochs': None,
    }

    # Close digag_filename
    result.store.close()

    # Close Dataset files
    train.store.close()
    test.store.close()

    return model_result_data