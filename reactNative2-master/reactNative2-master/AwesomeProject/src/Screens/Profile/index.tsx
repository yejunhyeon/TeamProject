import React, {useEffect, useState} from 'react';
import Styled from 'styled-components/native';
import Voice from '@react-native-community/voice';

const Container = Styled.View`
  flex: 1;
  justify-content: center;
  align-items: center;
  background-color: #EEEEEE;
`;
const View = Styled.View`
  width: 80%;
  height: 80%;
  background-color: #00AA0099;
  justify-content: center;
  align-items: center;
`;
const Text = Styled.Text`
  font-size: 42px;
  color: #000000;
`;
const ButtonRecord = Styled.Button``;

interface Props {
}

const Profile = ({}: Props) => {

  const [voice, setVoice] = useState<string>("--");
  const [isRecord, setIsRecord] = useState<boolean>(false);
  const buttonLabel = isRecord ? 'Stop' : 'Start';

  const onSpeechStart = (event: any) => {
    console.log('onSpeechStart');
    setVoice("");
  };

  const onSpeechEnd = (event: any) => {
    console.log('onSpeechEnd');
  };

  const onSpeechResults = (event: any) => {
    console.log('onSpeechResults');
    console.log(event);
    console.log(event.value[0]);
  };
  
  const onSpeechError = (event: any) => {
    console.log('onSpeechError');
    console.log(event);
  };

  const onRecordVoice = () => {
    if (isRecord) {
      Voice.stop();
    } else {
      Voice.start('en-US');
    }
    setIsRecord(!isRecord);
  };

  useEffect(() => {

    Voice.onSpeechStart = onSpeechStart;
    Voice.onSpeechEnd = onSpeechEnd;
    Voice.onSpeechResults = onSpeechResults;
    Voice.onSpeechError = onSpeechError;

    return () => {

      Voice.destroy().then(Voice.removeAllListeners);

    };

  },[]);

  return (
    <Container>
      <View>
        <Text>
          Profile / Voice
        </Text>
        <Text>
          {voice}
        </Text>
        <ButtonRecord onPress={onRecordVoice} title={buttonLabel} />
      </View>
    </Container>
  );
};

export default Profile;
