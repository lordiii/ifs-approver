```shell
# make image
docker build -t ifs-approver .

# run image
docker run -it --rm -p 5000:80 \
  -v $(pwd)/backend/ifsApprover:/ifs-backend/ifsApprover:ro \
  -v $(pwd)/backend/static-frontend:/ifs-backend/static-frontend:ro \
  -v $(pwd)/backend/cli:/ifs-backend/cli:ro \
  -v $(pwd)/backend/cgi:/ifs-backend/cgi:ro \
  -v $(pwd)/docker-support/config.py:/ifs-backend/config.py:ro \
  -v $(pwd)/docker-support/database.db:/ifs-backend/database.db \
  -v $(pwd)/docker-support/approved:/ifs-backend/approved \
    ifs-approver /bin/bash
```