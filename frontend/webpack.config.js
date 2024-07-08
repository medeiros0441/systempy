const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
    context: __dirname,
    entry: "./src/index.js",
    output: {
        path: path.resolve("./static/frontend/"),
        filename: "[name]-[hash].js",
    },
    plugins: [
        new BundleTracker({filename: "./webpack-stats.json"}),
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env", "@babel/preset-react"],
                    },
                },
            },
        ],
    },
    resolve: {
        extensions: [".js", ".jsx"],
    },
};
