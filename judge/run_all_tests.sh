for f in test/*/config.py ;
do
    
    echo $f;
    python3 prepare_task.py --test --config_path test/3/config.py 2>/dev/null | tail -n 1 ;
    echo ;

done