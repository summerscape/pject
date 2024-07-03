import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset
import torch.nn.functional as F

import weatherAPI

# 데이터 준비
X = np.array([
    [35, 80, 0, 5], [5, 60, 5, 3], [18, 50, 0, 2], [25, 90, 1, 8], [15, 40, 0, 1],
    [10, 55, 2, 4], [0, 30, 0, 10], [28, 70, 5, 2], [20, 60, 0, 6], [22, 80, 3, 7],
    [8, 65, 0, 5], [12, 50, 1, 3], [32, 85, 0, 9], [5, 90, 10, 5], [-5, 50, 0, 8],
    [30, 75, 0, 3], [25, 65, 1, 5], [18, 45, 0, 4], [10, 80, 5, 7], [2, 70, 0, 6],
    [29, 65, 2, 6], [18, 55, 1, 5], [6, 45, 0, 3], [21, 70, 3, 8], [10, 60, 1, 2],
    [14, 75, 4, 9], [24, 55, 0, 6], [30, 80, 2, 4], [22, 65, 1, 7], [16, 50, 0, 3],
    [5, 55, 5, 4], [28, 75, 3, 9], [12, 60, 0, 5], [8, 45, 1, 6], [20, 70, 2, 7],
    [15, 50, 0, 4], [6, 65, 5, 8], [25, 55, 1, 2], [17, 45, 0, 1], [5, 60, 5, 3]
])

y_upper = np.array([
    0, 2, 0, 1, 0, 2, 2, 0, 0, 1, 
    2, 0, 0, 2, 2, 0, 1, 0, 2, 2,
    3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 
    3, 4, 5, 6, 7, 8, 9, 0, 1, 2
])
y_lower = np.array([
    0, 2, 0, 1, 0, 2, 2, 0, 1, 1, 
    2, 0, 0, 2, 2, 0, 1, 0, 2, 2,
    3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 
    3, 4, 5, 6, 7, 8, 9, 0, 1, 2
])
y_shoes = np.array([
    2, 0, 1, 2, 1, 0, 1, 2, 1, 2, 
    1, 1, 2, 0, 1, 2, 2, 1, 1, 0,
    3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 
    3, 4, 5, 6, 7, 8, 9, 0, 1, 2
])

# 데이터 전처리
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 텐서로 변환
X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
y_upper_tensor = torch.tensor(y_upper, dtype=torch.long)
y_lower_tensor = torch.tensor(y_lower, dtype=torch.long)
y_shoes_tensor = torch.tensor(y_shoes, dtype=torch.long)

# 데이터셋 및 데이터로더 생성
dataset = TensorDataset(X_tensor, y_upper_tensor, y_lower_tensor, y_shoes_tensor)
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

# 모델 정의
class FashionModel(nn.Module):
    def __init__(self):
        super(FashionModel, self).__init__()
        self.common_layer1 = nn.Linear(4, 64)
        self.common_layer2 = nn.Linear(64, 32)
        self.upper_output = nn.Linear(32, 10)
        self.lower_output = nn.Linear(32, 10)
        self.shoes_output = nn.Linear(32, 10)
    
    def forward(self, x):
        x = F.relu(self.common_layer1(x))
        x = F.relu(self.common_layer2(x))
        upper = self.upper_output(x)
        lower = self.lower_output(x)
        shoes = self.shoes_output(x)
        return upper, lower, shoes

model = FashionModel()

# 손실 함수 및 옵티마이저 정의
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 모델 학습
num_epochs = 50
for epoch in range(num_epochs):
    model.train()
    for i, (inputs, y_upper, y_lower, y_shoes) in enumerate(dataloader):
        optimizer.zero_grad()
        outputs_upper, outputs_lower, outputs_shoes = model(inputs)
        loss_upper = criterion(outputs_upper, y_upper)
        loss_lower = criterion(outputs_lower, y_lower)
        loss_shoes = criterion(outputs_shoes, y_shoes)
        loss = loss_upper + loss_lower + loss_shoes
        loss.backward()
        optimizer.step()
    
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 모델 평가
model.eval()
with torch.no_grad():
    outputs_upper, outputs_lower, outputs_shoes = model(X_tensor)
    _, predicted_upper = torch.max(outputs_upper, 1)
    _, predicted_lower = torch.max(outputs_lower, 1)
    _, predicted_shoes = torch.max(outputs_shoes, 1)
    upper_accuracy = (predicted_upper == y_upper_tensor).sum().item() / len(y_upper_tensor)
    lower_accuracy = (predicted_lower == y_lower_tensor).sum().item() / len(y_lower_tensor)
    shoes_accuracy = (predicted_shoes == y_shoes_tensor).sum().item() / len(y_shoes_tensor)

print(f'상의 Accuracy: {upper_accuracy * 100:.2f}%')
print(f'하의 Accuracy: {lower_accuracy * 100:.2f}%')
print(f'신발 Accuracy: {shoes_accuracy * 100:.2f}%')


'''
 'PTY': '강수형태',
 'REH': '습도',
 'RN1': '1시간강수량',
 'T1H': '기온',
 'UUU': '동서바람성분',
 'VEC': '풍향',
 'VVV': '남북바람성분',
 'WSD': '풍속'

 '''



# 예측 및 출력
new_weather = np.array([[weatherAPI.t1h, weatherAPI.reh, weatherAPI.rn1, weatherAPI.wsd]])  # 온, 습도, 강수량, 풍속
new_weather_scaled = scaler.transform(new_weather)
new_weather_tensor = torch.tensor(new_weather_scaled, dtype=torch.float32)

model.eval()
with torch.no_grad():
    outputs_upper, outputs_lower, outputs_shoes = model(new_weather_tensor)
    upper_prediction = torch.argsort(outputs_upper, dim=1, descending=True).numpy()[0]
    lower_prediction = torch.argsort(outputs_lower, dim=1, descending=True).numpy()[0]
    shoes_prediction = torch.argsort(outputs_shoes, dim=1, descending=True).numpy()[0]

upper_labels = ['티셔츠', '블라우스', '점퍼', '셔츠', '니트', '후드', '재킷', '카디건', '스웨터', '폴로 셔츠']
lower_labels = ['청바지', '스커트', '정장바지', '반바지', '슬랙스', '치마바지', '레깅스', '조거팬츠', '미니스커트', '롱스커트']
shoes_labels = ['구두', '운동화', '슬리퍼', '로퍼', '샌들', '워커', '부츠', '스니커즈', '플랫슈즈', '힐']

# 스타일 매핑
upper_styles = {
    '티셔츠': '캐주얼', '블라우스': '클래식', '점퍼': '스포티', '셔츠': '클래식', '니트': '캐주얼',
    '후드': '스포티', '재킷': '클래식', '카디건': '캐주얼', '스웨터': '캐주얼', '폴로 셔츠': '캐주얼'
}
lower_styles = {
    '청바지': '캐주얼', '스커트': '캐주얼', '정장바지': '클래식', '반바지': '캐주얼', '슬랙스': '클래식',
    '치마바지': '캐주얼', '레깅스': '스포티', '조거팬츠': '스포티', '미니스커트': '캐주얼', '롱스커트': '캐주얼'
}
shoes_styles = {
    '구두': '클래식', '운동화': '스포티', '슬리퍼': '캐주얼', '로퍼': '클래식', '샌들': '캐주얼',
    '워커': '스포티', '부츠': '클래식', '스니커즈': '스포티', '플랫슈즈': '캐주얼', '힐': '클래식'
}



# 예측 결과 출력
styles = ['캐주얼', '클래식', '스포티']

print("추천 스타일")
for style in styles:
    upper_item = next(item for item in upper_prediction if upper_styles[upper_labels[item]] == style)
    lower_item = next(item for item in lower_prediction if lower_styles[lower_labels[item]] == style)
    shoes_item = next(item for item in shoes_prediction if shoes_styles[shoes_labels[item]] == style)

    print(f"\n스타일: {style}")
    print(f"상의 추천: {upper_labels[upper_item]} ({upper_styles[upper_labels[upper_item]]})")
    print(f"하의 추천: {lower_labels[lower_item]} ({lower_styles[lower_labels[lower_item]]})")
    print(f"신발 추천: {shoes_labels[shoes_item]} ({shoes_styles[shoes_labels[shoes_item]]})")
