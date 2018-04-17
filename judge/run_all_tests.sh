for f in test/*/config.py ;
do
    
    echo $f;
    python3 prepare_task.py --test --config_path $f 2>/dev/null | tail -n 1 ;
    echo ;

done
