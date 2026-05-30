import os
import glob
import pandas as pd
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import argparse
import numpy as np


def load_data(directory, data_type):
    pattern = os.path.join(directory, "**", data_type, "*.csv")
    list_files = glob.glob(pattern, recursive=True)

    data_list_prep = []
    for file in list_files:
        df = pd.read_csv(file, names=["measured_x", "measured_y", "real_x", "real_y"])
        data_list_prep.append(df)
    data_list = pd.concat(data_list_prep, ignore_index=True)
    measured_coords = data_list[["measured_x", "measured_y"]].values
    real_coords = data_list[["real_x", "real_y"]].values

    return measured_coords, real_coords

def standardization(measured_train, real_train, measured_test, real_test):
    scaler_measured = StandardScaler()
    scaler_real = StandardScaler()
    # Training set
    scaled_measured_train = scaler_measured.fit_transform(measured_train)
    scaled_real_train = scaler_real.fit_transform(real_train)
    # Testing set
    scaled_measured_test = scaler_measured.transform(measured_test)
    scaled_real_test = scaler_real.transform(real_test)

    return scaled_measured_train, scaled_real_train, scaled_measured_test, scaled_real_test, scaler_real

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='dane')
    parser.add_argument('--hidden_neurons', type=int, default=16)
    parser.add_argument('--activation_function', type=str, choices=['relu', 'tanh', 'sigmoid'], default='relu',)
    parser.add_argument('--learning_rate', type=float, default=0.01)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--num_rounds', type=int, default=5)

    args = parser.parse_args()
    directory = args.data_dir
    hidden_neurons = args.hidden_neurons
    activation_func = args.activation_function
    learning_rate = args.learning_rate
    epochs = args.epochs
    num_rounds = args.num_rounds

    measured_train, real_train = load_data(directory, 'stat')
    measured_test, real_test = load_data(directory, 'dyn')

    scaled_measured_train, scaled_real_train, scaled_measured_test, scaled_real_test, scaler_real = standardization(
        measured_train, real_train, measured_test, real_test
    )


    best_test_mse = float('inf')
    best_model = None
    best_history = None

    for round in range(num_rounds):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(units=hidden_neurons,
                                  activation=activation_func,
                                  input_shape=(2,)),
            tf.keras.layers.Dense(units=2)
        ])

        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        model.compile(optimizer=optimizer, loss='mse')

        history = model.fit(x = scaled_measured_train,
                            y = scaled_real_train,
                           validation_data=(scaled_measured_test, scaled_real_test),
                            batch_size=len(scaled_measured_train),
                            epochs=epochs)
        final_test_mse = history.history['val_loss'][-1]
        print(f"Błąd testowy MSE po {epochs} epokach: {final_test_mse:.4f}")

        if final_test_mse < best_test_mse:
            best_test_mse = final_test_mse
            best_model = model
            best_history = history.history

    history_filename = f"history_{activation_func}_{hidden_neurons}"
    df_mse = pd.DataFrame.from_dict(best_history)
    df_mse.to_csv(f'{history_filename}.csv', index=False)

    scaled_predictions = best_model.predict(scaled_measured_test)
    original_predictions = scaler_real.inverse_transform(scaled_predictions)

    prediction_filename = f"prediction_{activation_func}_{hidden_neurons}"
    df_preds = pd.DataFrame(original_predictions, columns=['Predicted_x', 'Predicted_y'])
    df_preds.to_csv(f'{prediction_filename}.csv', index=False)

    if not os.path.exists('error_mse_UWB.csv'):
        baseline_measured_scaled = scaler_real.transform(measured_test)
        baseline_mse = np.mean((scaled_real_test - baseline_measured_scaled) ** 2)
        df_err = pd.DataFrame({'Baseline_MSE': [baseline_mse]})
        df_err.to_csv('error_mse_UWB.csv', index=False)


if __name__ == "__main__":
    main()