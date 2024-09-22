# Gralx: Multimodal Context-Preserving Data Masking

The Multimodal Context-Preserving Data Masking API is an open-source privacy layer designed for companies building products on top of large public models or their own proprietary models. This API enables the seamless integration of advanced data masking techniques into existing applications, ensuring the protection of sensitive information while preserving the vital context necessary for accurate model performance.
Features


## Key Features

- **Seamless Integration:** The API provides a simple and intuitive interface for incorporating data masking capabilities into your existing pipelines, making it easy to protect sensitive data without extensive modifications to your codebase.
- **Multimodal Support:** The API supports various data modalities, including text, images, audio, and video, allowing you to protect sensitive information across different types of data utilized by your models.
- **Context-Preserving Masking:** Advanced masking techniques are employed to maintain the contextual integrity of the masked data, ensuring that the relationships and semantics within the dataset are preserved. This enables your models to perform accurately while safeguarding sensitive information.
- **Flexible Masking Strategies:** The API offers a range of masking strategies, such as substitution, encryption, and generalization, giving you the flexibility to choose the most appropriate technique for your specific use case and compliance requirements.
- **Customizable Masking Rules:** You can define custom masking rules based on your domain expertise and data privacy policies, ensuring that the masking process aligns with your organization's specific needs and regulations.
- **Performance Optimization:** The API is designed with performance in mind, leveraging efficient algorithms and parallel processing to minimize the impact on your application's runtime while delivering robust data protection.
Comprehensive Logging and Monitoring: Detailed logs and monitoring capabilities are provided to track the masking process, identify potential issues, and ensure the integrity of the masked data.

### Python Libraries
- Flask Security Too - authentification 
- PySceneDetect - split scenes

### External Frameworks 
- **[BMF (Babit Multimedia Framework)](https://babitmf.github.io/)developed by ByteDance:** Used to process the videos.
- **[Video LLaMa](https://github.com/DAMO-NLP-SG/Video-LLaMA)*:** Used to transcribe the video scene scene by scene.
- **Eleven Labs API:** Used to generated masked audio with swapped PII data variables.
- **[Presidio](https://microsoft.github.io/presidio/) by Mircrosoft:** Used to extract, label, and swap textual PII data.
- **Story Diffusion:** Used to generate frames that mask PII data but retain important context.
- **[EMO](https://github.com/HumanAIGC/EMO)by Alibaba:** used to re-animate facial expressions and lip-sync audio in the generated portraits 
- **[Animate Anyone](https://humanaigc.github.io/animate-anyone/) by Alibaba:** used to re-animate body movements in the generated images  
- 


