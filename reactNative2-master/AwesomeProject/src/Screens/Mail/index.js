import React, { Component } from 'react';
import { View, Alert, Button, StyleSheet } from 'react-native';
import Mailer from 'react-native-mail';

export default class App extends Component {

  render() {
    return (
      <View style={styles.container}>
        <Button
          onPress={() => {
            Mailer.mail({
              subject: 'need help', // 메일 제목
              recipients: ['btrya23@gmail.com'], // 수신 메일 리스트
              ccRecipients: ['supportCC@example.com'], // cc로 수신하는 이메일의 리스트 // 참고자
              bccRecipients: ['supportBCC@example.com'], // bcc로 수신하는 이메일의 리스트 // 비밀수신자
              body: '<b>A Bold Body</b>', // 이메일의 본문
              isHTML: true, // 이메일의 본문이 HTML 인지
              attachment: { // 첨부파일이 있는 경우
                path: '',  // 파일 위치
                type: '',   // Mime Type: jpg, png, doc, ppt, html, pdf, csv
                name: '',   // 사용자 정의 파일 이름 ??
              }
            }, (error, event) => {
              Alert.alert(
                error,
                event,
                [
                  {text: 'Ok', onPress: () => console.log('OK: Email Error Response')},
                  {text: 'Cancel', onPress: () => console.log('CANCEL: Email Error Response')}
                ],
                { cancelable: true }
              )
            });
          }}
          title="Email Me"
          color="#841584"
          accessabilityLabel="Purple Email Me Button"
        />
      </View>
    );
  }
}


const styles = StyleSheet.create({
  container: {
    padding: 16,
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  button: {
    alignItems: 'center',
    backgroundColor: '#DDDDDD',
    padding: 10,
    width: 300,
    margin: 10,
  },
  title: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  sliderContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    width: 300,
    padding: 5,
  },
  sliderLabel: {
    textAlign: 'center',
    marginRight: 20,
  },
  slider: {
    flex: 1,
  },
  textInput: {
    borderColor: 'gray',
    borderWidth: 1,
    color: 'black',
    width: 300,
    textAlign: 'center',
    height: 40,
  },
});