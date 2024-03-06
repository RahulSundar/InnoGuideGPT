# InnoGuideGPT


**InnoGuideGPT: Integrating conversational interface and
command interpretation for navigation robots** (Presented in the demo track at AIML systems in October 2023, Bangalore, Karnataka, India)

**Abstract**
Integrating natural language understanding, voice command interpretation and natural language generation for real-time inference is a challenging problem. However, developing a proof of concept is now
possible in just a few lines of code which was otherwise unimaginable a few years ago. Thanks to the democratization of LLMs and the availability of high-quality pre-trained models through APIs.
It is now possible to quickly build effective use cases by just integrating multiple models without even having to pre-train/fine-tune the models on custom data. This is due to their zero-shot learning ability. Although, there are many recent works in this regard oriented towards software [1, 5], edge implementations and their applications to Robotics are yet to be explored in their entirety [6]. Recently, Koubaa [2] proposed RoboGPT, where a ChatGPT was
prompt-tuned for command interpretation and subsequently determining the robot’s actions. In this work, we integrate a real-time conversational voice interface within a navigation robot. This is achieved using an underlying LLM interface to respond to user queries based on a prior context and additionally interpret voice commands for the robot to navigate. 

This repository currently consists only of the implementation of a speech-based LLM interface from the AIML systems conference paper:
Currently, details of the various clubs and projects at the Center For Innovation, IIT Madras have been provided as the context for RAG. A simple extraction chain has been further used to


Once the dependencies are installed, a StreamLit application has been built around the LLM interface that can be run locally
using :
```
streamlit run streamlit_app.py
```

If you found this code useful, please do star and cite the repository in your works:
```
@software{InnoguideGPT_2023,
  author        = "Rahul Sundar, Shreyash Gadgil, Tankala Satya Sai, Sathi Sai Krishna Reddy, Gautam B, Ishita Mittal, Jyotsna Sree Guduguntla",
  address       = "IBot club, CFI, IIT Madras, Chennai - 60036, India",
  title         = "LLM Interface codebase for InnoGuideGPT: Integrating conversational interface and
command interpretation for navigation robots",
  year          = "2023",
}
```


**Contributors to the LLM interface:**
1. Rahul Sundar: *Complete design, conception, implementation and project management*
2. Gautam: *Implementation and testing of the LLM*
3. Ishita: *Implementation and testing of the LLM*
4. Satya Sai:  *Conception, Data collection, project management*
5. Sai Krishna: *Conception, Data collection, project management*
6. Jyotsna: *ASR and TTS testing*
7. Shanmukesh: *ASR and TTS testing*

**Contributors to the conference paper:**
1. Rahul Sundar: *Complete design, conception (LLM interface), implementation and project management, Nvidia Jetson implementation*
2. Shreyash: *Nvidia Jetson implementation, ROS-based navigation bot route planning, and localization, project management*
3. Gautam: *Implementation and testing of the LLM*
4. Ishita: *Implementation and testing of the LLM*
5. Satya Sai:  * Conception, Nvidia Jetson implementation, navigation bot route planning and localization data collection, project management*
6. Sai Krishna: *Conception, Data collection, project management*
7. Jyotsna: *ASR and TTS testing*
8. Shanmukesh: *ASR and TTS testing*
