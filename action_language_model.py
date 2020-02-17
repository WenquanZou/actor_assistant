from torch import nn
import torch.nn.functional as F


class ActionModel:
    def __init__(self, num_classes):
        self.conv1 = nn.Conv3d(1, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv3d(64, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv3d(32, 16, kernel_size=3, padding=1)
        self.conv4 = nn.Conv3d(16, num_classes, kernel_size=3, padding=1)
    
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = self.conv4(x)
        return F.softmax(x, dim=1)


if __name__ == '__main__':
    from transformers import BertTokenizer, BertForQuestionAnswering
    import torch
    
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    
    question, text = "Who was Jim Henson?", "Jim Henson was a nice puppet"
    input_ids = tokenizer.encode(question, text)
    token_type_ids = [0 if i <= input_ids.index(102) else 1 for i in range(len(input_ids))]
    start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))
    print(start_scores)
    print(end_scores)
    all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer = ' '.join(all_tokens[torch.argmax(start_scores): torch.argmax(end_scores) + 1])
    print(answer)
    
    assert answer == "a nice puppet"