# Python Version

3.9 is fine for all problems except Question 8, which requires 3.7.

Requirements stored in `requirements.txt` in each folder (if applicable).

# Strucutre of Files

- Question 1
    - Part a - Q1/Q1a.py
      - Run `python Q1/Q1a.py`
    - Part b - Q1/Q1b.py
      - Run `python Q1/Q1b.py`
    - Part c - Q1/Q1c.py
      - Run `python Q1/Q1c.py`
- Question 2
  - Part a - Q2/Q2.md and Q2/Q2a.pdf
  - Part b - Q2/Q2.md
  - Part c - Q2/Q2.md and Q2/Q2c.py
    - Run `python Q2/Q2c.py`
- Question 3
  - Part a - Q3/Q3a.py and Q3/Q3a.md
    - Run `python Q3/Q3a.py`
  - Part b - Q3/Q3b.py
    - Run `python Q3/Q3b.py`
- Question 4
  - Part a - Q4/Q4a.md
  - Part b - Q4/Q4b.py, Q4/Q4b.md
    - Run `python Q4/Q4b.py`
  - Part c - Q4/Q4c.py, Q4/Q4c.md
    - Run `python Q4/Q4c.py`
- Question 5
  - part a - Q5/Q5a.md
  - part b - Q5/Q5b.png, Q5/A5b.md
  - part c - Q5/Q5c.py, Q5/model.obj and Q5/Q5 train Q learn model.py
    - Train the model first by running `python "Q5/Q5 train Q learn model.py"` After training has completed, run `python Q5/Q5c.py`
- Question 6
    -Run the collab ipynb files
  - part a - Q6/Q6a.ipynb
  - part b - Q6/Q6b_output.mp4 and Q6/Q6bc.ipynb
  - part c - Q6/Q6bc.ipynb
- Question 7
  - part a - Q7/Q7.md and Q7/Q7.py (other models are called their respective names)
    - To Run A*, run `python Q7/a_star_with_timestamps.py`
    - To run BFS, run `python Q7/bfs_with_timestamps.py`
    - To run Dijkstras, run `python Q7/dijkstra_with_timestamps.py`
    - To run RRT*, run `python Q7/rrt_star_with_timestamps.py`
    - To run RRT, run `python Q7/rtt.py`
    - To run the maze, run `python Q7/Q7.py`
- Question 8
  - part a - Q8/8A/Q8a.py
    - Run `Q8/8A/Q8a.py`
  - part b - Q8/8B/
    - From within 8B run `python yolov5/train.py --batch 16 --epochs 5 --data dataset.yaml --weights '' --cfg yolov5s.yaml`
      - Edit the batch size, number of epochs, and add a `--workers <x>` argument depending on hardware specs and desired time to run.
    - Results will be displayed in terminal, additionally, graphics will be placed in `Q8/8B/yolo5/runs/train/exp<x>`.
    - The highest value after (exp) will be the most recent data to use.
    - The best model will be found in `Q8/8B/yolov5/runs/train/exp<x>/weights/best.pt`
    - Additionally, view training graphically by running `tensorboard --logdir yolov5/runs/` from a different shell session and accessing `localhost:6006` in a web browser.
    - Text result of findings is found in `results.txt`
  - part c -Q8/8C
    - From within 8C run `python yolov5/train.py --data cats_and_dogs.yaml --weights yolov5s.pt --epochs 5 --batch 16 --freeze 10`
      - As before, edit the arguments according to system specifications
- Question 9
  - parts a-d - Q9/Q9.md


