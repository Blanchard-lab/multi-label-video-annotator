**Multi-Label Video Annotation Tool**

Annotating videos manually is annoying but often necessary for supervised learning workflows. This is a tool orginally written to help annotate videos for multi-label classification quickly. It offers flexibility on crafting labels and selecting them. Labels are saved automatically as JSON files with the same name as the video files.

This tools is continuously developing. More annotation options will be added as needed. If you are interested in object annotation, check out [this](https://github.com/Blanchard-lab/LegoStructureAnnotationTool) tool from labmates Changsoo and Jack.

**Setup**

```conda env create -f environment.yml```

```conda activate mlva```

**How to run**

```python mlva.py```
