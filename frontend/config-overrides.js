const path = require('path');
const { override } = require('customize-cra');

module.exports = override(
  (config) => {
    config.resolve.alias = {
      ...(config.resolve.alias || {}),
      src: path.resolve(__dirname, 'src')
    };
    return config;
  }
);
