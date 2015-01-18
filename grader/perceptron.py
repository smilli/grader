class MulticlassPerceptron():

    def __init__(self, features):
        """
        Constructor for MulticlassPerceptron

        Params:
        features (string[]) - list of feature names
        """
        self.clf = BinaryPerceptron(features)
        self.training_feats = []
        self.pos_target_names = []
        self.correct_targets = []

    def train(self, training_feats, pos_target_names, correct_targets, num_iter=5):
        """
        Train the Perceptron.

        Params:
        training_feats (dict{feature_name: value}[][]) -
           A list of tests.  Each test is a list of dict mappings of all
           features for the different possible targets.
        pos_target_names (string[][]) - The names of the pos targets for each dict
            mapping of features.
        correct_targets (string[]) - The correct target for each test.
        num_iter (int) - The number of times to do the training.
        """
        # assumes train is only called once for each piece of
        # training data
        new_training_feats = []
        for test_feats in training_feats:
            new_feats = []
            for feats in test_feats:
                new_feats.append(self.clf.feature_dict_to_list(feats))
            new_training_feats.append(new_feats)
        self.training_feats.extend(new_training_feats)
        self.pos_target_names.extend(pos_target_names)
        self.correct_targets.extend(correct_targets)
        self._train(num_iter)

    def _train(self, num_iter=5):
        for _ in range(num_iter):
            for (feats, pos_target_names, correct_target) in zip(
                    self.training_feats, self.pos_target_names,
                    self.correct_targets):
                correct_ind = pos_target_names.index(correct_target)
                all_preds = self.clf.predict(feats)
                pred_ind = max(enumerate(all_preds), key=lambda x: x[1])[0]
                if pred_ind != correct_ind:
                    incorrect_feats = feats[pred_ind]
                    correct_feats = feats[correct_ind]
                    weight_changes = [c - i for c, i in zip(correct_feats,
                        incorrect_feats)]
                    self.clf.update_weights(weight_changes)

    def predict(self, data_feats, pos_target_names):
        """
        Return list of predictions for given data.

        Params:
        data_feat(dict{feature_name: value}[][]) -
           A list of tests.  Each test is a list of dict mappings of all
           features for the different possible targets.
        pos_target_names (string[][]) - The names of the pos targets for each dict
            mapping of features.
        """
        print(self.clf.feature_weights)
        predictions = []
        for (feats, pos_target_names) in zip(data_feats, pos_target_names):
            feats = [self.clf.feature_dict_to_list(f) for f in feats]
            all_preds = self.clf.predict(feats)
            pred_ind = max(enumerate(all_preds), key=lambda x: x[1])[0]
            predictions.append(pos_target_names[pred_ind])
        return predictions

    def reset(self):
        self.clf.reset()
        self.training_feats = []
        self.pos_target_names = []
        self.correct_targets = []


class BinaryPerceptron():

    def __init__(self, features):
        """
        Constructor for binary perceptron.

        Params:
        features (string[]) - list of features
        """
        self.features_to_ind = dict((y, x) for x,y in enumerate(features))
        self.feature_weights = [0] * len(features)
        self.num_features = len(features)
        self.training_data = []
        self.training_targets = []

    def update_weights(self, weight_changes):
        """
        Updates weights.

        Params:
        weight_changes (int[]) - the list of changes to add to each weight
        """
        self.feature_weights = [w + c for w, c in 
                zip(self.feature_weights, weight_changes)]

    def predict(self, data_feats):
        """
        Returns list of scores for list of features.

        Params:
        data_feats (int[[]]) - list of list of features for each possible target
        """
        scores = []
        for feature_vals in data_feats:
            score = sum(v*w for v, w in zip(feature_vals, self.feature_weights))
            scores.append(score)
        return scores

    def feature_dict_to_list(self, feats):
        feature_values = [0] * self.num_features
        for name, value in feats.items():
            feature_values[self.features_to_ind[name]] = value
        return feature_values

    def _predict(self, feats):
        """
        Returns score for features.

        Params:
        feats (dict{feature_name: value}) - dict of feature name & value pairs
        """
        feature_vals = self.feature_dict_to_list(feats)
        return sum(v*w for v, w in zip(feature_vals, self.feature_weights))

    def reset(self):
        self.feature_weights = [0] * self.num_features
        self.training_data = []
        self.training_targets = []
