#! /bin/bash

## 1 to 2
# ssb -> rest
./scripts/model/eval_extra_features.sh job,tpcds ssb
mv results/model_eval/extra_features results/model_eval/extra_features_ssb\>job,tpcds
# job -> rest
./scripts/model/eval_extra_features.sh ssb,tpcds job
mv results/model_eval/extra_features results/model_eval/extra_features_job\>ssb,tpcds
# tpcds -> rest
./scripts/model/eval_extra_features.sh ssb,job tpcds
mv results/model_eval/extra_features results/model_eval/extra_features_tpcds\>ssb,job

## 2 to 1
# rest -> ssb
./scripts/model/eval_extra_features.sh ssb job,tpcds
mv results/model_eval/extra_features results/model_eval/extra_features_job,tpcds\>ssb
# rest -> job
./scripts/model/eval_extra_features.sh job ssb,tpcds
mv results/model_eval/extra_features results/model_eval/extra_features_ssb,tpcds\>job
# rest -> tpcds
./scripts/model/eval_extra_features.sh tpcds ssb,job
mv results/model_eval/extra_features results/model_eval/extra_features_ssb,job\>tpcds

## Individual
# ssb -> job
./scripts/model/eval_extra_features.sh job ssb
mv results/model_eval/extra_features results/model_eval/extra_features_ssb\>job
# ssb -> tpcds
./scripts/model/eval_extra_features.sh tpcds ssb
mv results/model_eval/extra_features results/model_eval/extra_features_ssb\>tpcds
# job -> ssb
./scripts/model/eval_extra_features.sh ssb job
mv results/model_eval/extra_features results/model_eval/extra_features_job\>ssb
# job -> tpcds
./scripts/model/eval_extra_features.sh tpcds job
mv results/model_eval/extra_features results/model_eval/extra_features_job\>tpcds
# tpcds -> ssb
./scripts/model/eval_extra_features.sh ssb tpcds
mv results/model_eval/extra_features results/model_eval/extra_features_tpcds\>ssb
# tpcds -> job
./scripts/model/eval_extra_features.sh job tpcds
mv results/model_eval/extra_features results/model_eval/extra_features_tpcds\>job
