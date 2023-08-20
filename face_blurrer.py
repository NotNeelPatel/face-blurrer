from PIL import Image, ImageFilter, ImageDraw
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import sys

def blur(image,detection_result, output):

  im = image

  for detection in detection_result.detections:
    # Create bounding box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height

    # Create mask
    mask = Image.new('L', im.size, 255)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([ (start_point), (end_point) ], fill=0)
    mask.save('mask.png')

    # Gaussian Blur with intensity based on size of bounding box
    blurred = im.filter(ImageFilter.GaussianBlur((bbox.height // 100) ** 3 + 5))
    blurred.paste(im, mask=mask)
    im = blurred
    blurred.save(output)
    os.remove('mask.png')

def blur_image(file_name, output):
  create_output = Image.open(file_name)
  create_output.save(output)
  # Load the input image.
  image = mp.Image.create_from_file(file_name)
  # Detect faces in the input image.
  detection_result = detector.detect(image)
  # Process the detection result. In this case, visualize it.
  blur(create_output, detection_result, output)

base_options = python.BaseOptions(model_asset_path='detector.tflite')
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)

if __name__ == "__main__":
  file_name = sys.argv[1]
  file_split = file_name.split('.')
  output = f'{file_split[0]}_blurred.{file_split[1]}'
  
  if len(sys.argv) > 2:
    output = sys.argv[2]
  blur_image(file_name,output)
