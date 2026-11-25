# Car Counter (OpenCV)

Counts vehicles crossing a virtual line in a traffic video using
background subtraction (MOG2) and centroid tracking. Built with Python and OpenCV only, no deep learning.

## How it works
1. MOG2 learns the road background and isolates moving objects
2. Morphological operations remove noise and fill holes in the blobs
3. Contours give one bounding box per vehicle
4. Each blob centroid is matched to the nearest centroid from the previous frame
5. A vehicle is counted when its centroid crosses the counting line (both directions)

## Setup
```bash
pip install -r requirements.txt
python download_video.py
python counter.py
```

`download_video.py` downloads a sample video into `video/`.
The video is not stored in this repository.

## Controls
| Key | Action |
|---|---|
| `w` | move the counting line up |
| `s` | move the counting line down |
| `q` | quit |

## Parameters (in `counter.py`)
| Name | Meaning |
|---|---|
| `MIN_AREA` | blobs smaller than this (in pixels) are ignored |
| `MAX_DIST` | maximum centroid movement between two frames |
| `varThreshold` | MOG2 sensitivity |

## Results
| Video segment | Manual count | Program count | Error |
|---|---|---|---|
| (fill in) | | | |

## Limitations
- Touching vehicles merge into one blob and are counted once
- Stopped vehicles slowly fade into the background
- The tracker is simple: a vehicle missed for one frame loses its ID
- No vehicle classification (car, truck, ...)

## Possible next step
Replace the detector with YOLO and a tracker such as ByteTrack, then compare accuracy with this version.

## Video source
Sample video from the
[OpenCV_3_Car_Counting_Cpp](https://github.com/MicrocontrollersAndMore/OpenCV_3_Car_Counting_Cpp)
repository. Not included in this repo.
