curl -H 'content-type:application/json' -d '{"message": "http://localhost:8082/root.add_worker"}' http://localhost:8083/worker.add_to_root

#curl -H 'content-type:application/json' -d '{"message": "http://looktwits-root.appspot.com/root.add_worker"}' http://looktwits-worker-1.appspot.com/worker.add_to_root
