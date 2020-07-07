module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  plugins: [                        // root-import 추가
    [                               //
      'babel-plugin-root-import',   //
      {                             //
        rootPathPerfix: '~',        //
        rootPathSuffix: 'src',      //
      },                            //
    ],                              //
  ],                                //
};
