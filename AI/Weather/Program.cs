using System;
using System.IO;
using System.Linq;
using NumSharp;
using Tensorflow;
using Tensorflow.Keras.ArgsDefinition;
using Tensorflow.Keras.Layers;
using Tensorflow.Keras.Engine;
using Tensorflow.Keras.Optimizers;
using static Tensorflow.Binding;

namespace TemperatureForecastTFNET
{
    public static class NDArrayExtensions
    {
        // Converts a flat 1D array to jagged array [rows][cols]
        public static T[][] ToJaggedArray<T>(this T[] flatData, int rows, int cols)
        {
            var jagged = new T[rows][];
            for (int i = 0; i < rows; i++)
            {
                jagged[i] = new T[cols];
                Array.Copy(flatData, i * cols, jagged[i], 0, cols);
            }
            return jagged;
        }
    }

    class TempForecastLoader
    {
        public static (NDArray, NDArray) LoadForTemperatureForecast(string path)
        {
            var lines = File.ReadAllLines(path);
            var data = lines.Skip(1).Select(l => l.Split(',').ToArray()).ToArray();

            int numSamples = data.Length - 1;
            int numFeatures = data[0].Length - 2;

            var x = np.zeros((numSamples, numFeatures));
            var y = np.zeros((numSamples, 1));

            for (int i = 0; i < numSamples; i++)
            {
                for (int j = 2; j < data[i].Length; j++)
                    x[i, j - 2] = float.Parse(data[i][j]);

                y[i, 0] = float.Parse(data[i + 1][3]);
            }

            return (x, y);
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            var (x_train, y_train) = TempForecastLoader.LoadForTemperatureForecast("data/solar_weather.csv");

            // Convert NDArray -> flattened -> jagged arrays
            float[][] xJagged = x_train.astype(np.float32).GetData<float>()ToJaggedArray(x_train.shape[0], x_train.shape[1]);
            float[][] yJagged = y_train.astype(np.float32).GetData<float>().ToJaggedArray(y_train.shape[0], y_train.shape[1]);

            Tensor X = tf.constant(xJagged);
            Tensor Y = tf.constant(yJagged);

            // Build layers
            var hidden1Layer = new Dense(new DenseArgs { Units = 64 });
            var hidden2Layer = new Dense(new DenseArgs { Units = 32 });
            var outputLayer = new Dense(new DenseArgs { Units = 1 });

            var optimizer = new Adam(0.001f);

            int epochs = 500;
            for (int step = 0; step < epochs; step++)
            {
                using var tape = tf.GradientTape();

                // Forward pass with ReLU activations
                var h1 = tf.nn.relu(hidden1Layer.Apply(X));
                var h2 = tf.nn.relu(hidden2Layer.Apply(h1));
                var y_pred = outputLayer.Apply(h2);

                var loss = tf.reduce_mean(tf.square(y_pred - Y));

                // Collect trainable variables
                var trainableVars = new Layer[] { hidden1Layer, hidden2Layer, outputLayer }
                    .SelectMany(layer => layer.TrainableVariables)
                    .ToArray();

                var grads = tape.gradient(loss, trainableVars);
                optimizer.apply_gradients(zip(grads, trainableVars));

                if (step % 50 == 0)
                    Console.WriteLine($"Step {step}, Loss = {loss.numpy()}");
            }

            // Predict next temperature using last row
            var lastRow = x_train[x_train.shape[0] - 1];
            var lastX = tf.constant(np.expand_dims(lastRow.astype(np.float32), 0)); // [1, numFeatures]

            var h1_last = tf.nn.relu(hidden1Layer.Apply(lastX));
            var h2_last = tf.nn.relu(hidden2Layer.Apply(h1_last));
            var prediction = outputLayer.Apply(h2_last);

            Console.WriteLine($"Predicted future temp = {prediction.numpy()[0, 0]}");
        }
    }
}
