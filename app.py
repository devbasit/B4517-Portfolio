from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Helper function to read Excel files
def load_excel_data(filename):
    try:
        df = pd.read_excel(filename)
        return df.to_html(classes='table table-striped', index=False)
    except:
        return "<p>Error loading table data</p>"

@app.route('/')
def home():
    return render_template('index.html', 
        page_title="ABDULSALAM BASIT ML PORTFOLIO",
        content="""
        <p>My public ML portfolio.<br>
        This portfolio contains description of some selected projects majorly computer vision projects on different areas including classification and segmentation.</p>
        <p>Contact<br>
        Email: <a href="mailto:basitsalam2001@gmail.com">basitsalam2001@gmail.com</a><br>
        Phone: <a href="tel:+2347050837042">+2347050837042</a></p>
        <p>A copy of my CV can be accessed at <a href="https://docs.google.com/document/d/1abzvZSsUPLYUKVUf_qC6vZPpm_ByAZr3/edit?usp=sharing&ouid=109569805470530100719&rtpof=true&sd=true">CV [gdrive link]</a></p>
        <img src="/static/how-to-build-a-machine-learning-portfolio.jpeg" class="img-fluid" alt="Portfolio Image">
        """,
        active_page='Home')

@app.route('/project1')
def project1():
    return render_template('index.html', 
        page_title="ABDULSALAM BASIT ML PORTFOLIO",
        content="""
        <h2 class="text-center">UNet Optimized With Differential Evolution</h2>
        <p>The key goal of the project was to optimize a UNet segmentation model such that we can have a small model size which will still perform as excellent as any other SoTA segmentation models.<br>
        The models compared with were SEGNET, PSPNET, and FCN.<br>
        The model achieved a weights size of about 5mb in contrast to others that are in the range of tens and hundreds mb.<br>
        The training data used was potato leaves downloaded from plant village which included Healthy, Early Blight and Late blight. Training was done using just early blight but models were evaluated on all 3 classes. Annotations were done manually.</p>
        <h4>Tools Used:</h4>
        <ol>
            <li>VGG IMAGE ANNOTATOR</li>
            <li>TENSORFLOW</li>
            <li>PYTHON</li>
            <li>NUMPY</li>
            <li>STREAMLIT</li>
            <li>OpenCV etc</li>
        </ol>
        <h4>Project Highlight:</h4>
        <ul>
            <li>Performed data engineering.</li>
            <li>Optimized a UNet to have small parameters and low model size.</li>
            <li>Achieved good metrics on the segmentation task. MIoU > 75%</li>
            <li>Implemented a streamlit interface for visualizing predictions</li>
        </ul>
        <img src="/static/VIA in use.png" class="img-fluid" alt="VIA in use" style="max-width: 100%;">
        <p class="text-center"><small>VIA IN USE</small></p>
        """,
        active_page='Project 1')

@app.route('/project2')
def project2():
    table_html = load_excel_data('project2 sample table.xlsx')
    return render_template('index.html', 
        page_title="ABDULSALAM BASIT ML PORTFOLIO",
        content=f"""
        <h2 class="text-center">UNet with Pretrained Encoders and Optimized With Differential Evolution</h2>
        <p>The key objectives of the project was to optimize a number of UNet segmentation architectures with pretrained encoders like VGG19 and so on with differential evolution.<br>
        In the project, some layers of the encoder of a standard Unet architecture were replaced with pretrained weights from different models.<br>
        Next step was to optimize the layers of the decoder using differential evolution and record the values.<br>
        The training data used for the project include leaves of maize, cassava, yam etc.<br>
        In comparing the models, each model is trained 6 times. A training involve training on 4 crops and evaluating on the 5th crop. The 6th training is done by combining all the crops and splitting<br>
        In the end, VGG19 model optimized at decoder layer 4 proved to be the best model on the task.</p>
        <h4>Tools Used:</h4>
        <ol>
            <li>VGG IMAGE ANNOTATOR</li>
            <li>Adobe photoshop (for removing unwanted noises in the images used)</li>
            <li>TENSORFLOW</li>
            <li>PYTHON</li>
            <li>NUMPY</li>
            <li>STREAMLIT</li>
            <li>OpenCV etc</li>
        </ol>
        <h4>Project Highlight:</h4>
        <ul>
            <li>Performed data engineering.</li>
            <li>Replaced layers of the encoder with pretrained weights</li>
            <li>Optimized layers of the decoders to have small parameters, low model size and good performance.</li>
            <li>Achieved good metrics on the segmentation task. MIoU > 75%</li>
            <li>Implemented a streamlit interface for visualizing predictions</li>
        </ul>
        <p>A SAMPLE OF THE REPORT AND STREAMLIT INTERFACES ARE SHOWN BELOW. Further enquiry can be checked in the <a href="https://docs.google.com/document/d/1roWh0Jl_VcngLd_OmuGMlIP2hdXSJRbf/edit?usp=drivesdk&ouid=109569805470530100719&rtpof=true&sd=true">report [gdrive link]</a> or by contacting me</p>
        <h4 class="text-center">Project main report</h4>
        {table_html}
        <img src="/static/project2 sample interface.png" class="img-fluid" alt="Project 2 interface">
        <h4 class="text-center">Sample predictions from the models</h4>
        <img src="/static/project2 outputs.png" class="img-fluid" alt="Project 2 outputs">
        """,
        active_page='Project 2')

@app.route('/project3')
def project3():
    return render_template('index.html', 
        page_title="ABDULSALAM BASIT ML PORTFOLIO",
        content="""
        <h2 class="text-center">SCIZOPHRENIA DETECTION MODEL</h2>
        <p>The main goal of the project is to develop a schizophrenia detection model with EfficientNet.<br>
        The data used was retrieved from schizconnect and processed using matlab dpabi/dparsf and SPI</p>
        <p>Further enquiry can be checked in the <a href="https://docs.google.com/document/d/1-2tQln0dTxbZkHM7kayoc9dcnRcICnUD/edit?usp=drivesdk&ouid=109569805470530100719&rtpof=true&sd=true">report [gdrive link]</a> or by contacting me</p>
        <h4>Tools Used:</h4>
        <ol>
            <li>SCHIZOPHRENIA</li>
            <li>OPENCV</li>
            <li>TENSORFLOW</li>
            <li>PYTHON</li>
            <li>NUMPY</li>
            <li>SimpleITK</li>
            <li>DLTK</li>
            <li>MATLAB</li>
            <li>DPABI</li>
        </ol>
        <h4>Project Highlight:</h4>
        <ul>
            <li>Performed data engineering.</li>
            <li>PROCESSED MRI DATA</li>
            <li>TRAINED EFFICIENTNET MODELS</li>
        </ul>
        <h4 class="text-center">Project Visualizations</h4>
        <img src="/static/project3 data collection.png" class="img-fluid" alt="Data Acquisition">
        <p class="text-center"><small>DATA ACQUISITION</small></p>
        <img src="/static/project3 dpabi proessing.png" class="img-fluid" alt="DPABI Processing">
        <p class="text-center"><small>DPABI PROCESSING</small></p>
        <img src="/static/project3 processed images.png" class="img-fluid" alt="Processed Images">
        <p class="text-center"><small>PROCESSED IMAGES</small></p>
        """,
        active_page='Project 3')

@app.route('/project4')
def project4():
    table_html = load_excel_data('project4 sample table.xlsx')
    return render_template('index.html', 
        page_title="ABDULSALAM BASIT ML PORTFOLIO",
        content=f"""
        <h2 class="text-center">Tiny Segmentation Network</h2>
        <p>The key requirement of the project was to build a small model for segmenting plant leaves. The model should be small enough to be deployed on a microcontroller but also powerful enough to perform up to task.<br>
        In the project, the model mimicked a standard unet but the approach used was utilizing a deeper model and creating different decoder networks for each class and then combining the outputs at the inference.<br>
        The training data used for the project include leaves of maize, cassava, yam etc., all featuring different types of diseases.<br>
        For evaluation, the model was first evaluated against other standard Unet architectures with pretrained encoders and then with other SoTA segmentation models.<br>
        In the end, the model had a total model size of 8mb and it performed the best on the task.</p>
        <h4>Tools Used:</h4>
        <ol>
            <li>VGG IMAGE ANNOTATOR</li>
            <li>Adobe photoshop (for removing unwanted noises in the images used)</li>
            <li>TENSORFLOW</li>
            <li>PYTHON</li>
            <li>NUMPY</li>
            <li>STREAMLIT</li>
            <li>OpenCV etc</li>
            <li>FLUTTER</li>
        </ol>
        <h4>Project Highlight:</h4>
        <ul>
            <li>Performed data engineering.</li>
            <li>Created a tiny segmentation model.</li>
            <li>Achieved good metrics on the segmentation task. MIoU > 80%</li>
            <li>Implemented a streamlit interface for visualizing predictions</li>
            <li>Deployed The model on an android phone</li>
        </ul>
        <p>A SAMPLE OF THE REPORT AND OTHER MODEL VISUALIZATIONS ARE SHOWN BELOW. Further enquiry can be checked in the <a href="https://docs.google.com/document/d/1ZuVrWaqN7Jhi-rECwiz1xBuiiiA-LPCU/edit?usp=drivesdk&ouid=103980037459622424907&rtpof=true&sd=true">report [gdrive link]</a> or by contacting me</p>
        <h4 class="text-center">Project main report</h4>
        {table_html}
        <h4 class="text-center">Sample predictions from the models</h4>
        <img src="/static/project4 outputs.png" class="img-fluid" alt="Project 4 outputs">
        <h4 class="text-center">Model visualization</h4>
        <div class="row">
            <div class="col-md-6">
                <img src="/static/project4 novel outlook.jpg" class="img-fluid" alt="Model outlook">
                <p class="text-center"><small>model outlook</small></p>
            </div>
            <div class="col-md-6">
                <img src="/static/project4 NOVEL MODEL ARCHITECTURE.png" class="img-fluid" alt="Model architecture">
                <p class="text-center"><small>model arch</small></p>
            </div>
        </div>
        <h4 class="text-center">Android App</h4>
        <img src="/static/segmenterApp.jpg" class="img-fluid" alt="Android deployment">
        <p class="text-center"><small>Android deployment</small></p>
        """,
        active_page='Project 4')

@app.route('/project5')
def project5():
    table_html = load_excel_data('project5 sample table.xlsx')
    return render_template('index.html', 
        page_title="ABDULSALAM BASIT ML PORTFOLIO",
        content=f"""
        <h2 class="text-center">Tiny Segmentation and Classification Network</h2>
        <p>The goal of the project was to build a small model for segmenting and classifying plant leaves. The model should be small enough to be deployed on a microcontroller but also powerful enough to perform up to task.<br>
        In the project, a classification model was built and then integrated with the segmentation model built in the prior project.<br>
        In building the classification model, some concepts used were
        <ul>
            <li>THE USE OF WIDE NETWORKS</li>
            <li>THE USE OF DEEP NETWORKS</li>
            <li>THE USE OF INCEPTION MODULES</li>
            <li>THE USE OF RESIDUAL CONNECTIONS</li>
            <li>THE USE OF 1x1 CONVOLUTIONS</li>
            <li>THE USE OF CNN INSTEAD OF DENSE NETWORKS</li>
        </ul>
        The training data used for the project include leaves of maize, cassava, yam etc., all featuring different types of diseases as in the case of the segmentation model.<br>
        For evaluation, the classification model was evaluated against some other SoTA classification models.<br>
        In the end, the classification model had a total model size of &lt;400kb and it performed the best on the task but second best to Densenet pretrained model.</p>
        <h4>Tools Used:</h4>
        <ol>
            <li>VGG IMAGE ANNOTATOR</li>
            <li>Adobe photoshop (for removing unwanted noises in the images used)</li>
            <li>TENSORFLOW</li>
            <li>PYTHON</li>
            <li>NUMPY</li>
            <li>STREAMLIT</li>
            <li>OpenCV etc</li>
            <li>FLUTTER</li>
        </ol>
        <h4>Project Highlight:</h4>
        <ul>
            <li>Performed data engineering.</li>
            <li>Created a tiny classification model.</li>
            <li>Achieved good metrics on the segmentation task. F1 score > 98%</li>
            <li>Implemented a streamlit interface for visualizing predictions</li>
            <li>Deployed The model on an android phone</li>
        </ul>
        <p>A SAMPLE OF THE REPORT AND OTHER MODEL VISUALIZATIONS ARE SHOWN BELOW. Further enquiry can be checked in the <a href="https://docs.google.com/document/d/1X0QJ3VesoOagpyS5ptqLvy3sjBW9Tb18/edit?usp=drivesdk&ouid=103980037459622424907&rtpof=true&sd=true">report [gdrive link]</a> or by contacting me</p>
        <h4 class="text-center">Project main report</h4>
        {table_html}
        <img src="/static/project5 sample interface.png" class="img-fluid" alt="Project 5 interface">
        <h4 class="text-center">Model visualization</h4>
        <div class="row">
            <div class="col-md-6">
                <img src="/static/project5 large.png" class="img-fluid" alt="Model large">
                <p class="text-center"><small>model large</small></p>
            </div>
            <div class="col-md-6">
                <img src="/static/project5 small.png" class="img-fluid" alt="Model small">
                <p class="text-center"><small>model small</small></p>
            </div>
        </div>
        <h4 class="text-center">Android App</h4>
        <img src="/static/segClassApp.jpg" class="img-fluid" alt="Android deployment">
        <p class="text-center"><small>Android deployment</small></p>
        """,
        active_page='Project 5')

@app.route('/project6')
def project6():
    return render_template('index.html', 
        page_title="ABDULSALAM BASIT ML PORTFOLIO",
        content="""
        <h2 class="text-center">ARDUINO/ML AFib DETECTION</h2>
        <p>AN ECG ACQUISITION SYSTEM. The raw ECG is taken using AD8232 sensor with Arduino at 500Hz sampling frequency and stored in an array. Peaks are obtained from the array and features extracted. The extracted features are fed into a RandomForestClassifier model already built using scikit learn and converted to C++ using micromlgen python library.<br>
        The model was trained to detect Normal Sinus Rhythm, AFib and Other Heart diseases. The model prediction will be displayed on an LCD screen. The ecg array and extracted features will be saved on SD card and can be used on a streamlit app to display some information.<br>
        Anticipate!!!</p>
        """,
        active_page='Project 6(nearing final stages)')

@app.route('/project7')
def project7():
    return render_template('index.html', 
        page_title="ABDULSALAM BASIT ML PORTFOLIO",
        content="""
        <h2 class="text-center">NEURAL TRANSLATION AND AUDIO GENERATION</h2>
        <p>ANTICIPATE!!!<br>
        It is a system that takes audio directly from a microphone, transcribes it, translate to other languages, transforms the translated texts to audio, send over bluetooth with raspberry to multiple bluetooth speakers with each speaker handling specific language.</p>
        """,
        active_page='Project 7(ongoing)')

if __name__ == '__main__':
    app.run(debug=True)