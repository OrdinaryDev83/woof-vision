import React, {Component, useState} from 'react';
import {StyleSheet, TouchableOpacity, Text, View, Image} from 'react-native';
import * as ImagePicker from 'expo-image-picker';

export default function App () {
  const [image,setImage]=useState(null);
  const [result,setResult]=useState("...");

  const pickImageCamera = async () => {
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();
    if (permissionResult.granted === false) {
      alert("You've refused to allow this app to access your camera");
      return;
    }
    let result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsMultipleSelection: false,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 1,
    });
  
    if (!result.canceled) {
      displayImage(result.assets[0].uri);
    }
  };
  
  const pickImageGallery = async () => {
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (permissionResult.granted === false) {
      alert("You've refused to allow this app to access your gallery");
      return;
    }
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsMultipleSelection: false,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 1,
    });
  
    if (!result.canceled) {
      displayImage(result.assets[0].uri);
    }
  };

  const sendImage = async (image) => {
    console.log("sending image...", image.substring(0, 100));
    call_post(image);
  }

  return (
    // temporary ugly react
    <View style={styles.container}>
      {image && <Image source={{uri:image}} style={{marginLeft:'auto',width:400,height:400,marginRight:'auto'}} />}
      <Text/>
      <TouchableOpacity style={styles.button} onPress={pickImageCamera}>
          <Text>Camera</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.button} onPress={pickImageGallery}>
        <Text>Gallery</Text>
      </TouchableOpacity>
      <Text>Select a Photo</Text>
      <Text></Text>
      <Text></Text>
      <Text></Text>
      <Text></Text>
      <Text></Text>
      <TouchableOpacity style={styles.button} onPress={analyze}>
        <Text>Analyze</Text>
      </TouchableOpacity>
      <Text></Text>
      <Text>Results</Text>
      <Text></Text>
      <Text>{result}</Text>
    </View>
  );

  function toDataUrl(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
        var reader = new FileReader();
        reader.onloadend = function() {
            callback(reader.result);
        }
        reader.readAsDataURL(xhr.response);
    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();
  }
  
  function displayImage(uri) {
    toDataUrl(uri, function(myBase64) {
      setImage(myBase64);
    });
  }
  
  function analyze() {
    sendImage(image);
  }
  
  function call_post(base64) {
    console.log(base64.substring(0, 100));
    fetch('http://10.0.2.2:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image : base64
      }),
    })
    .then(async (response) => {
      let data = await response.json();
      console.log('Success:', JSON.stringify(data).substring(0, 100));
      try{
        process_response(data);
      } catch(e) {
        console.log(e);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }

  function process_response(response_json) {
    var p = "";
    var dict = response_json["prediction"];
    console.log(dict);
    for (const [key, value] of Object.entries(dict)) {
      if (value > 0.1)
      {
        p += `${key} ${(value * 100.0).toFixed(2)}%\n`;
      }
    }

    setResult(p);
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  button: {
    alignItems: 'center',
    backgroundColor: '#DDDDDD',
    padding: 10,
    marginBottom: 10,
  },
});