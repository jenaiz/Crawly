curl -H \
   'content-type:application/json' \
   -d '{"message": "http://www.insanedata.com,http://www.jenaiz.com"}'\
   http://localhost:8083/worker.job
