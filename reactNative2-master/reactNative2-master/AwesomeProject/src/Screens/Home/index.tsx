import React, {useEffect, useState} from 'react';
import Styled from 'styled-components/native';
import DeviceInfo from 'react-native-device-info';

// import Tts from 'react-native-tts';
// var Speech = require('react-native-speech');

const Container = Styled.View`
  flex: 1;
  justify-content: center;
  align-items: center;
  background-color: #EEEEEE;
`;
const View = Styled.View`
  width: 80%;
  height: 80%;
  background-color: #0000AA99;
  justify-content: center;
  align-items: center;
`;
const Text = Styled.Text`
  font-size: 24px;
  color: #000000;
  margin: 8px;
`;
const ButtonRecord = Styled.Button``;

interface Props {
}

const Home = ({}: Props) => {

  const [ID, setID] = useState<string>("");
  const [Tablet, setTablet] = useState<boolean>(false);
  
  
  useEffect(() => {
    
    const uniqueID = DeviceInfo.getUniqueId();
    const isTablet = DeviceInfo.isTablet();
    
    if(setID){
      setID(uniqueID);
    }
    if(isTablet){
      setTablet(isTablet);
    }

    return () => {
    };
  },[]);

  return (
    <Container>
      <View>
        <Text>
          Home / DeviceInfo
        </Text>
        <Text>
          uniqueID
        </Text>
        <Text style={{ width:300, fontSize:20, textAlign:"center"}}>
          {ID}
        </Text>
        <Text>
        isTablet {Tablet}
        </Text>
        <ButtonRecord onPress={() => {
          console.log("button push");
        }} 
        title={"buttonLabel"}/>
      </View>
    </Container>
  );
};

export default Home;
