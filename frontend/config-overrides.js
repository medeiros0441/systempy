const path = require('path');
const { override } = require('customize-cra');

module.exports = override((config) => {
  // Adicione ou atualize os aliases existentes
  config.resolve.alias = {
    ...(config.resolve.alias || {}),
    src: path.resolve(__dirname, 'src'), // Alias para a pasta src
    '@objetos': path.resolve(__dirname, 'src/components/objetos'),
    '@components': path.resolve(__dirname, 'src/components'),
    '@containers': path.resolve(__dirname, 'src/components/containers'),
    '@assets': path.resolve(__dirname, 'src/assets'),
    '@interface': path.resolve(__dirname, 'src/interface'),
    '@routes': path.resolve(__dirname, 'src/routes'),
    '@services': path.resolve(__dirname, 'src/services'),
    '@utils': path.resolve(__dirname, 'src/utils'),
  };
  return config;
});
