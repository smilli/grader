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
        self.training_feats.extend(training_feats)
        self.pos_target_names.extend(pos_target_names)
        self.correct_targets.extend(correct_targets)
        self._train(num_iter)

    def _train(self, num_iter=5):
        for _ in range(num_iter):
            for (feats, pos_target_names, correct_target) in zip(
                    self.training_feats, self.pos_target_names,
                    self.correct_targets):
                correct_ind = post_target_names.index(correct_target)
                assert (correct_ind > -1)
                all_preds = self.clf.predict(feats)
                pred_ind = max(enumerate(all_preds), key=lambda x: x[1])[0]
                if pred_ind != correct_ind:
                    incorrect_feats = feats[pred_ind]
                    correct_feats = feats[correct_ind]
                    weight_changes = [c - i for c, i in zip(correct_feats,
                        incorrect_feats)]
                    clf.update_weights(weight_changes)


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
        predictions = []
        for (feats, pos_target_names) in zip(
                self.training_feats, self.pos_target_names,
                self.correct_targets):
            all_preds = self.clf.predict(feats)
            pred_ind = max(enumerate(all_preds), key=lambda x: x[1])[0]
            predictions.append(pos_target_names[pred_ind])
        return predictions


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
        self.weights = [w + c for w, c in zip(self.weights, weight_changes)]

    def predict(self, data_feats):
        """
        Returns list of list of scores.

        Params:
        data_feats (dict{feature_name: value}[][]) - list of list of features
            for each possible target
        """
        for feats in data_feats:
            return [predict(feat) for feat in feats]

    def feature_dict_to_list(self, feat):
        feature_values = [0] * self.num_features
        for name, value in feats.items():
            feature_values[self.features_to_ind[name]] = value

    def _predict(self, feats):
        """
        Returns score for features.

        Params:
        feats (dict{feature_name: value}) - dict of feature name & value pairs
        """
        feature_vals = feature_dict_to_list(self, feat)
        return sum(v*w for v, w in zip(feature_vals, feature_weights))
