# OpenCV tracking

Python module for multitracking objects over any given video. Mainly tested on tracking players over a football field.

## Usage

After cloning the repo just build the docker image

```
docker build . -t tracker
```

and run it with the desired parameters

```
docker run -v "$PWD":/host_volume -w /app tracker:latest \
        -input_path <input video filepath> \
        -input_bbox_path <input bbox json filepath> \
        -output_path <output video filepath> \
        -method <tracking method>
```

In which

- `<input video filepath>`: filepath for a mp4 video to annotate.
- `<input bbox json filepath>`: filepath for a json file with initial bbox information. The json is expected to be a list of dictionaries with the following keys:
  - Name: String. Name of the object to track. i.e 'player'
  - Id: Int. Id of the object to track.
  - Coords: List of 4 ints determining the bounding box position and size: x, y, width, height
- `<output video filepath>`: filepath for the output mp4 file to save.
- `<tracking method>`: tracking method, should be one of the following `['dasiamrpn', 'tld', 'kcf', 'goturn', 'csrt', 'mil', 'boosting', 'mosse', 'medianflow']`

** Note: ** The volume `/host_volume` is mounted to allow input and output paths from outside the container. See [this](https://flaviocopes.com/docker-access-files-outside-container/) for more info.

For example:

```
docker run -v "$PWD":/app tracker:latest \
        -input_path /app/data/messi1.mp4 \
        -input_bbox_path /app/data/messi1_initial_conditions.json \
        -output_path /app/output/messi1_tracked.mp4 \
        -method csrt
```

**Note:** The recommended method for the given test files is CSRT.

## Testing

To test the script with all 4 available videos and all available methods, build the docker image

```
docker build . -t tracker
```

and run it with the `-test` flag, which executes the pytest module

```
docker run -v "$PWD":/app tracker:latest -test
```

**Note:** When a tracking method fails to track an objet at least 70% of the frames, pytest will issue a warning. This can happen for less accurate methods like MedianFlow.

## Supported methods

- [DaSiamRPN](https://arxiv.org/abs/1808.06048)
- [TLD](http://vision.stanford.edu/teaching/cs231b_spring1415/papers/Kalal-PAMI.pdf)
- [KCF](https://arxiv.org/abs/1404.7584)
- [GoTurn](https://davheld.github.io/GOTURN/GOTURN.pdf)
- [CSRT](https://arxiv.org/pdf/1611.08461.pdf)
- [MIL](https://ieeexplore.ieee.org/document/5206737)
- [Boosting](http://www.bmva.org/bmvc/2006/papers/033.pdf)
- [Mosse](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf)
- [MedianFlow](http://kahlan.eps.surrey.ac.uk/featurespace/tld/Publications/2010_icpr.pdf)

## Comparative examples: Boosting vs CSRT vs MedianFlow

We test a small subset of all methods over three videos.

### Example 1: Multiple tracking

Method: Boosting

![boosting](https://user-images.githubusercontent.com/8797947/158618364-1ee7a2c3-6dbf-436f-a977-189ecfff0bd2.gif)

Method: CSRT

![csrt](https://user-images.githubusercontent.com/8797947/158618498-f302f98c-859f-41d1-91bc-3ac7fb09b4f0.gif)

Method: MedianFlow

![medianflow](https://user-images.githubusercontent.com/8797947/158618604-bbec4535-07f0-48c1-bf5c-2d91cc6787f4.gif)

### Example 2: Managing occlusions

Method: Boosting

![boosting](https://user-images.githubusercontent.com/8797947/158605699-55e7a70b-99cc-4631-a265-ee06edb03f48.gif)

Method: CSRT

![csrt](https://user-images.githubusercontent.com/8797947/158605701-1440aa63-68de-4ba5-9b12-442b93b78020.gif)

Method: MedianFlow

![medianflow](https://user-images.githubusercontent.com/8797947/158605711-372af741-0285-4d18-9b9a-f103a6a18201.gif)

### Example: Managing occlusions, grainy picture and zoom

Method: Boosting

![boosting](https://user-images.githubusercontent.com/8797947/158619166-edc83759-406a-4902-a355-0e256274fb57.gif)

Method: CSRT

![csrt](https://user-images.githubusercontent.com/8797947/158619238-efd38e13-75bf-4622-8569-43eb8030abe1.gif)

Method: MedianFlow

![medianflow](https://user-images.githubusercontent.com/8797947/158619367-4d5971dc-7ef1-4544-9338-e96a2b13259f.gif)
