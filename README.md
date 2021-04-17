# Local playground for Logica

* Fork the repo, so you can add your personal notebooks or modify the demo notebook.
* Clone your repo to local machine
* In the repo dir, build docker image
  ```
  docker build . -f docker/playground.Dockerfile -t playground
  ```
* Run the docker image which 1) mounts the notebook directory in the repo and 2) spawns a Jupyter server
  ```
  docker run -it --rm -p 8888:8888 -v $HOME/git/datalogdb/notebook:/notebook playground
  ```
  Here, we assume the repo dir is `$HOME/git/datalogdb`

* Notice the console output and copy the link to browser and open the `demo.ipynb` notebook.
