


<README_PA2>_2015004693_양상헌

Simplescene.py 파일 편집 부분
- display()
- onMouseDrag()
- onMouseButton() 
- 그외 필요한 전역변수 & 행렬


[A]: UI
	-(1) 첫실행시 cow는 클릭되지 않은 상태이다.
	-(2) cow를 처음 한번 클릭하면 drag 를 인식하는 상태가되고 Horizontal Drag 상태가 되고 cow가 커서를 따라 움직인다.
	-(2-1) 마우스를 누르고 있는 상태에선 vertical drag가 활성화된다
	-(3) 마우스를 눌렀다가 떼는순간 cow의 위치가 저장이되고 다시 (2)번 상태가 된다.
	-(4) cow 6개가 정해지면 롤러코스터 이동이 3번 실행된다.
	-(5) (4)번이 완료되면 다시 (1)번 상태로 돌아간다. 이때 cow 의 위치는 롤러코스터 이동이 끝났을때의 위치이다. 


[B]: Vertical Drag & Horizontal Drag & display()
	- onMouseButton(), onMouseDrag() 이 두함수를 많이 편집하여 구현했다.
	- onMouseButton()함수에서 선택된 cow의 정보를 따로 만들어논 배열에 저장하는 일을 한다.
	- - 드래깅이 활성화된 상태에서 마우스버튼이 올라올때 cow의 정보(이때의 cow2wld)를 배열에 저장하게 되고, cow의 숫자를 새서 6개까지 저장하게 된다.
	- vertical dragging의 경우 horizontal과 비슷한 구조로 구현되었다.
	- - 크게 다른점은 plane을 x축이 법선 벡터인 평면(y,z평면)으로 만들고 ray와 그 평변이 만나는 점을 계산한뒤, 계산된 점의 x좌표와 z좌표를 고정시켜서 y좌표값만 변화하게 만들어주었다.
	- dragging후 cow의 위치를 선택한후 선택된 곳에서 cow의 drag움직임이 시작할수 있도록 pickInfo를 수정해주는 부분도 vertical drag와 horizontal Drag에 추가해 주었다.
	- 선택된 cow가 6개가 된경우 drag를 비활성화 시키고 롤러코스터 에니메이션이 실행될수 있도록 만들었다.
	- 에니메이션이 종료되면 초기상태로 돌아가게 된다.
	- display()함수 내부를 많이 편집했는데 선택된 cow의 숫자가 6개 미만일땐 선택한 위치들에 cow를 표시하다가 6개가 다 채워지면 cow를 다 지우고 get_time()함수를 이용해서 t 를 계산한후 t 값에 따라 변화하는 위치에만 cow를 표시 하였다. animStartTime이라는 전역변수를 두고 이 변수는 cow가 6개 채워지면 get_time()으로 초기화 되고 이후 get_time()을 호출할때는 animStartTime 값을 빼줘 0~18초 까지 계산이 될수 있도록 하였다.


[C]: Catmull-Rom spline curve 애니메이션 구현방법
	- PDF에 있는 catmull-rom 행렬 공식을 그대로 사용하였다.
	- 포인트값은 저장된 cow2wld 행렬의 translate부분(4번째 culumn)만을 따와 사용하였다. 
	- 행렬 공식 대입으로 t값에 따른 포인트를 계산하여 cow2wld행렬 4번째 culumn에 대입후 t값에 따라 변화하는 cow2wld를 drawcow()의 인자로 사용 하였다.
	- t 값은 get_time()함수를 이용하여 구하고 18초(6초씩 3바퀴)까지 구하게 된다.(여기서 점과 다음점 사이를 이동하는 시간을 1초로 생각)
	- 이로인해 cow의 위치가 변하는 애니메이션 구현이 가능했다.
	- 하지만 이때의 움직이는 cow의 얼굴 방향은 아직 고정 상태이다. 

	
[D,E]: Cow의 얼굴 방향을 진행방향과 같게 만들기. display()
	- cow가 움직이는 과정에서 변화하는 t값에 따른 위치를 나타내는 t에 관한 3차 방정식을 미분하면 그 위치에서의 접선(방향벡터)를 구할수 있음을 이용하여 방향뻭터를 일단 구했다. 
	- - 행열연산에서 t행렬을 (t^3,t^2,t,1) => (3t^2, 2t ,1, 0)으로 바꿔 계산하였다.
	- 그후 cross product방식을 사용 하여 cow의 local coordinate를 바꿔주려하였다.
	- - 앞서 구한 방향벡터를 cow의 local x축으로 만들어준다.
	- - local z축 = cross(local x축, up(0,1,0)) -> cow의 바뀐 local z축.
	- - local y축 = cross(local z축, local x축) -> cow의 바뀐 local y축. 
	- - 이후 [x축, y축, z축, 0]인 4x4 행렬을 만들고 이를 inverse, transepose 한다음에 기존에 구해놨던 cow2wld에 곱해준다. 순서는 cow2wld @ M(inv).T 이다.
	- - 이 결과 , cow의 방향이 일정해지긴 했는데 머리가 아닌 옆구리가 이동방향을 바라보게 되어서 local y축을 기준으로 -90도 회전시켜주어야 겠다고 생각하고 , YR(y축기준으로 -90도 회전 행렬)을 제작하여 곱해주었다.
	- - 처음 시도할때 순서는 cow2wld @ M(inv).T @ YR.T 였다.
	- - 이 시도의 결과는 틀린 결과였고, 순서를 바꾸어 cow2wld @ YR.T @ M(inv).T 로 수정후 확인해본 결과 맞는 결과가 나왔다. local coordinate에서는 rotation을 먼저 실행 해주는 게 맞는 결과이기 때문이었던것 같다.
