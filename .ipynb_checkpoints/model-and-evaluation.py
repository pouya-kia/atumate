import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report,\
    roc_auc_score
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN, Birch
from kmodes.kprototypes import KPrototypes
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score, davies_bouldin_score
from fcmeans import FCM
from scipy.spatial.distance import cdist

# Function to standardize data
def standardize_data(df):
    print("Choose a standardization method:")
    print("1. Standard Scaler (zero mean, unit variance)")
    print("2. Min-Max Scaler (scale features to a range [0, 1])")
    print("3. Robust Scaler (scale features using median and IQR)")
    method_choice = input("Enter the number of the method: ").strip()

    if method_choice == '1':
        scaler = StandardScaler()
    elif method_choice == '2':
        scaler = MinMaxScaler()
    elif method_choice == '3':
        scaler = RobustScaler()
    else:
        print("Invalid choice. Defaulting to Standard Scaler.")
        scaler = StandardScaler()

    return pd.DataFrame(scaler.fit_transform(df), columns=df.columns)


# Function to calculate Dunn Index
def dunn_index_score(df, labels):
    # Get unique cluster labels
    unique_clusters = np.unique(labels)

    # Step 1: Compute intra-cluster distances (maximum distance within each cluster)
    intra_cluster_distances = []
    for cluster in unique_clusters:
        # Select points in the current cluster
        cluster_points = df[labels == cluster]
        if len(cluster_points) > 1:
            # Compute pairwise distances within the cluster
            distances = cdist(cluster_points, cluster_points, metric='euclidean')
            # Take the maximum distance within the cluster
            max_intra_cluster_distance = np.max(distances)
            intra_cluster_distances.append(max_intra_cluster_distance)

    # Step 2: Compute inter-cluster distances (minimum distance between different clusters)
    inter_cluster_distances = []
    for i, cluster_i in enumerate(unique_clusters):
        for j, cluster_j in enumerate(unique_clusters):
            if i < j:  # Only compute for distinct pairs of clusters
                points_i = df[labels == cluster_i]
                points_j = df[labels == cluster_j]
                # Compute pairwise distances between the two clusters
                distances = cdist(points_i, points_j, metric='euclidean')
                # Take the minimum distance between the two clusters
                min_inter_cluster_distance = np.min(distances)
                inter_cluster_distances.append(min_inter_cluster_distance)

    # Step 3: Calculate the Dunn Index
    if intra_cluster_distances and inter_cluster_distances:
        dunn_index = min(inter_cluster_distances) / max(intra_cluster_distances)
        return dunn_index
    else:
        return 0.0  # Return 0 if there are no valid distances



# Function to choose feature selection method
def choose_feature_selection_method():
    print("Choose feature selection method:")
    print("1. Supervised Learning")
    print("2. Unsupervised Learning")
    choice = input("Enter the number corresponding to your choice: ").strip()

    if choice == '1':
        return 'supervised'
    elif choice == '2':
        return 'unsupervised'
    else:
        print("Invalid choice. Defaulting to supervised learning.")
        return 'supervised'


# Supervised learning workflow
def supervised_learning(df):
    # Ask for the target column
    target_column = input("Enter the target column: ").strip()

    # Drop the target column from features
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Standardization
    standardize = input("Do you want to standardize the data? (yes/no): ").strip().lower()
    if standardize == 'yes':
        X = standardize_data(X)

    # Ask user to choose a model
    print("Choose a supervised learning model:")
    print("1. Logistic Regression")
    print("2. K-nearest Neighbors")
    print("3. Support Vector Machine")
    print("4. Decision Trees Classifier")
    print("5. Random Forest Classifier")
    print("6. XGBoost Classifier")
    model_choice = input("Enter the number of the model: ").strip()

    # Ask user if they want to split data into train/test sets
    split_data = input("Do you want to split the data into train/test sets? (yes/no): ").strip().lower()
    if split_data == 'yes':
        test_size = float(input("Enter the test size as a fraction (e.g., 0.2): ").strip())
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    else:
        X_train, X_test, y_train, y_test = X, X, y, y

    # Choose model and ask for parameters (if any)
    model = None
    if model_choice == '1':
        print("Logistic Regression selected.")
        model = LogisticRegression()
    elif model_choice == '2':
        print("K-nearest Neighbors selected.")
        n_neighbors = int(input("Enter the number of neighbors (default=5): ") or 5)
        model = KNeighborsClassifier(n_neighbors=n_neighbors)
    elif model_choice == '3':
        print("Support Vector Machine selected.")
        kernel = input("Enter kernel type (linear, poly, rbf, default=rbf): ").strip() or 'rbf'
        model = SVC(kernel=kernel)
    elif model_choice == '4':
        print("Decision Trees Classifier selected.")
        max_depth = input("Enter the max depth of the tree (default=None): ")
        model = DecisionTreeClassifier(max_depth=int(max_depth) if max_depth else None)
    elif model_choice == '5':
        print("Random Forest Classifier selected.")
        n_estimators = int(input("Enter the number of trees (default=100): ") or 100)
        model = RandomForestClassifier(n_estimators=n_estimators)
    elif model_choice == '6':
        print("XGBoost Classifier selected.")
        learning_rate = float(input("Enter the learning rate (default=0.1): ") or 0.1)
        model = XGBClassifier(learning_rate=learning_rate)

    # Train model
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.4f}")

    # Ask user for evaluation method
    print("Choose evaluation method:")
    print("1. Accuracy")
    print("2. Precision, Recall, F1-score")
    print("3. ROC-AUC")
    print("4. All methods")
    eval_choice = input("Enter the number of the evaluation method: ").strip()

    # Implement evaluation methods based on user choice
    metrics = {
        "Accuracy": accuracy,
        "Precision": precision_score(y_test, y_pred, average='weighted'),
        "Recall": recall_score(y_test, y_pred, average='weighted'),
        "F1-Score": f1_score(y_test, y_pred, average='weighted')
    }

    if eval_choice == '1':
        print(f"Accuracy: {metrics['Accuracy']:.4f}")
    elif eval_choice == '2':
        print(f"Precision: {metrics['Precision']:.4f}")
        print(f"Recall: {metrics['Recall']:.4f}")
        print(f"F1-Score: {metrics['F1-Score']:.4f}")
    elif eval_choice == '3':
        if len(set(y)) == 2:  # Check if binary classification
            roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
            print(f"ROC-AUC Score: {roc_auc:.4f}")
        else:
            print("ROC-AUC is only applicable for binary classification.")
    elif eval_choice == '4':
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")

        if len(set(y)) == 2:  # Check if binary classification
            roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
            print(f"ROC-AUC Score: {roc_auc:.4f}")
        else:
            print("ROC-AUC is only applicable for binary classification.")

        # Print detailed classification report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))


def unsupervised_learning(df):
    # Ask for data standardization
    standardize = input("Do you want to standardize the data? (yes/no): ").strip().lower()
    if standardize == 'yes':
        df = standardize_data(df)

    while True:  # Loop to allow multiple model evaluations
        print("Choose an unsupervised learning model:")
        print("1. K-Means")
        print("2. DBSCAN")
        print("3. K-Prototypes")
        print("4. K-Medoids")
        print("5. FCM")
        print("6. BIRCH")
        print("7. Exit")
        model_choice = input("Enter the number of the model: ").strip()

        labels = None  # Variable to hold labels for evaluation

        if model_choice == '1':
            print("K-Means selected.")
            detect_k = input("Do you want to detect 'k' using Elbow Method? (yes/no): ").strip().lower()

            if detect_k == 'yes':
                # Elbow method
                distortions = []
                K = range(1, 10)
                for k in K:
                    kmeans = KMeans(n_clusters=k)
                    kmeans.fit(df)
                    distortions.append(kmeans.inertia_)

                # Plot elbow curve
                plt.figure(figsize=(8, 6))
                plt.plot(K, distortions, 'bx-')
                plt.xlabel('k')
                plt.ylabel('Distortion')
                plt.title('Elbow Method For Optimal k')
                plt.show()

                k = int(input("Choose the number of clusters from the elbow plot: ").strip())
            else:
                k = int(input("Enter the number of clusters (k): ").strip())

            kmeans = KMeans(n_clusters=k)
            kmeans.fit(df)
            labels = kmeans.labels_

        elif model_choice == '2':
            print("DBSCAN selected.")
            # Set default values for DBSCAN parameters
            default_eps = 0.5
            default_min_samples = 5

            eps_input = input(f"Enter the value for epsilon (eps) (default: {default_eps}): ").strip()
            min_samples_input = input(
                f"Enter the minimum number of samples in a neighborhood (default: {default_min_samples}): ").strip()

            eps = float(eps_input) if eps_input else default_eps
            min_samples = int(min_samples_input) if min_samples_input else default_min_samples

            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            dbscan.fit(df)
            labels = dbscan.labels_

        elif model_choice == '3':
            print("K-Prototypes selected.")
            n_clusters = int(input("Enter the number of clusters: ").strip())
            categorical_columns = input("Enter the categorical column names separated by commas: ").strip().split(',')
            categorical_columns = [col.strip() for col in categorical_columns]
            kproto = KPrototypes(n_clusters=n_clusters, init='Huang')
            labels = kproto.fit_predict(df, categorical=categorical_columns)

        elif model_choice == '4':
            print("K-Medoids selected.")
            n_clusters = int(input("Enter the number of clusters: ").strip())
            kmedoids = KMedoids(n_clusters=n_clusters)
            kmedoids.fit(df)
            labels = kmedoids.labels_

        elif model_choice == '5':
            print("Fuzzy C-Means Clustering selected.")
            n_clusters = int(input("Enter the number of clusters: ").strip())
            fcm = FCM(n_clusters=n_clusters)
            fcm.fit(df)
            labels = fcm.predict(df)

        elif model_choice == '6':
            print("BIRCH selected.")
            brc = Birch()
            brc.fit(df)
            labels = brc.labels_

        elif model_choice == '7':
            print("Exiting the unsupervised learning workflow.")
            break

        else:
            print("Invalid model choice. Please try again.")
            continue  # Restart the loop if the choice is invalid

        # Evaluate the model
        print("Choose an evaluation method:")
        print("1. Silhouette Score")
        print("2. Dunn Index")
        print("3. Number of Clusters (for DBSCAN only)")
        eval_choice = input("Enter the number of the evaluation method: ").strip()

        if eval_choice == '1' and model_choice == '1':  # K-Means
            silhouette_avg = silhouette_score(df, labels)
            print(f"Silhouette Score for K-Means: {silhouette_avg:.4f}")

        elif eval_choice == '1' and model_choice in ['2', '4', '5', '6']:  # Other models
            print("Silhouette Score is not applicable for this model.")

        elif eval_choice == '2':  # Dunn Index for all models
            dunn_index = dunn_index_score(df, labels)
            print(f"Dunn Index: {dunn_index:.4f}")

        elif eval_choice == '3' and model_choice == '2':  # Number of clusters for DBSCAN
            num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            print(f"Number of clusters found by DBSCAN: {num_clusters}")

        else:
            print("Invalid evaluation method choice.")

        # Ask to allocate labels
        allocate_labels = input("Do you want to allocate labels to the DataFrame? (yes/no): ").strip().lower()
        if allocate_labels == 'yes':
            if model_choice == '1':
                df['KMeans_Labels'] = labels
            elif model_choice == '2':
                df['DBSCAN_Labels'] = labels
            elif model_choice == '3':
                df['KPrototypes_Labels'] = labels
            elif model_choice == '4':
                df['KMedoids_Labels'] = labels
            elif model_choice == '5':
                df['FCM_Labels'] = labels
            elif model_choice == '6':
                df['BIRCH_Labels'] = labels

        # Ask if the user wants to try another model
        try_another_model = input("Do you want to train with another model? (yes/no): ").strip().lower()
        if try_another_model == 'no':
            print("Exiting the unsupervised learning workflow.")
            break

    # At the end, show the DataFrame with labels if any
    print("Final DataFrame with allocated labels:")
    print(df)
