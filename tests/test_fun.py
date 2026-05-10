from httpx import AsyncClient

async def test_create_task(ac: AsyncClient):
    response = await ac.post('/task/', json={
        'title': '1 test task',
        'description': 'description',
        'status': 'waiting',
        'priority': 1
    })
    assert response.status_code == 200
    assert response.json() == {'status': 'success'}
    response = await ac.post('/task/', json={
        'title': '2 test task',
        'description': 'description',
        'status': 'in progress',
        'priority': 2
    })
    assert response.status_code == 200
    assert response.json() == {'status': 'success'}

async def test_create_task_error(ac: AsyncClient):
    response = await ac.post('/task/', json={
        'title': '3 test task',
        'description': 'description',
        'status': 'ab',
        'priority': 'gh'
    })
    assert response.status_code == 422

async def test_read_task(ac: AsyncClient):
    response = await ac.get('/task/')
    assert response.status_code == 200

async def test_read_task_title(ac: AsyncClient):
    response = await ac.get('/task/title/1 test task')
    assert response.status_code == 200
    assert response.json()[0][1] == '1 test task'
    assert response.json()[0][2] == 'description'
    assert response.json()[0][3] == 'waiting'
    assert response.json()[0][4] == 1

async def test_read_task_title_empty(ac: AsyncClient):
    response = await ac.get('/task/title/12')
    assert response.status_code == 200
    assert response.json() == []

async def test_read_task_id(ac: AsyncClient):
    response = await ac.get('/task/id/1')
    assert response.status_code == 200
    assert response.json()[0][1] == '1 test task'
    assert response.json()[0][2] == 'description'
    assert response.json()[0][3] == 'waiting'
    assert response.json()[0][4] == 1

async def test_read_task_id_error(ac: AsyncClient):
    response = await ac.get('/task/id/ty')
    assert response.status_code == 422


async def test_up_task(ac: AsyncClient):
    response = await ac.put('/task/1 test task', json={
        'title': '1 test task',
        'description': 'update description',
        'status': 'ok',
        'priority': 0
    })
    assert response.status_code == 200
    assert response.json() == {'status': 'success'}

async def test_sort_task_title(ac: AsyncClient):
    response = await ac.get('/task/sort/?by=title')
    assert response.status_code == 200
    assert response.json()[0][1] <= response.json()[1][1]

async def test_sort_task_error(ac: AsyncClient):
    response = await ac.get('/task/sort/')
    assert response.status_code == 422

async def test_sort_task_title_desc(ac: AsyncClient):
    response = await ac.get('/task/sort/?by=title&desc=true')
    assert response.status_code == 200
    assert response.json()[0][1] >= response.json()[1][1]

async def test_sort_task_description(ac: AsyncClient):
    response = await ac.get('/task/sort/?by=description')
    assert response.status_code == 200
    assert response.json()[0][2] <= response.json()[1][2]

async def test_sort_task_description_desc(ac: AsyncClient):
    response = await ac.get('/task/sort/?by=description&desc=true')
    assert response.status_code == 200
    assert response.json()[0][2] >= response.json()[1][2]

async def test_sort_task_status(ac: AsyncClient):
    response = await ac.get('/task/sort/?by=status')
    assert response.status_code == 200
    assert response.json()[0][3] <= response.json()[1][3]

async def test_sort_task_status_desc(ac: AsyncClient):
    response = await ac.get('/task/sort/?by=status&desc=true')
    assert response.status_code == 200
    assert response.json()[0][3] >= response.json()[1][3]

async def test_sort_task_priority(ac: AsyncClient):
    response = await ac.get('/task/sort/?by=priority')
    assert response.status_code == 200
    assert response.json()[0][4] <= response.json()[1][4]

async def test_sort_task_priority_desc(ac: AsyncClient):
    response = await ac.get('/task/sort/?by=priority&desc=true')
    assert response.status_code == 200
    assert response.json()[0][4] >= response.json()[1][4]

async def test_sort_task_date(ac: AsyncClient):
    response = await ac.get('/task/sort/?by=date')
    assert response.status_code == 200
    assert response.json()[0][5] <= response.json()[1][5]

async def test_sort_task_date_desc(ac: AsyncClient):
    response = await ac.get('/task/sort/?by=date&desc=true')
    assert response.status_code == 200
    assert response.json()[0][5] >= response.json()[1][5]

async def test_search_task(ac: AsyncClient):
    response = await ac.get('/task/search/?s=update')
    assert response.status_code == 200
    assert response.json()[0][1] == '1 test task'
    assert response.json()[0][2] == 'update description'
    assert response.json()[0][3] == 'ok'
    assert response.json()[0][4] == 0

async def test_search_task_empty(ac: AsyncClient):
    response = await ac.get('/task/search/?s=tre')
    assert response.status_code == 200
    assert response.json() == []

async def test_top_task(ac: AsyncClient):
    response = await ac.get('/task/top/2/')
    assert response.status_code == 200
    assert response.json()[0][1] == '2 test task'
    assert response.json()[0][2] == 'description'
    assert response.json()[0][3] == 'in progress'
    assert response.json()[0][4] == 2
    assert response.json()[1][1] == '1 test task'
    assert response.json()[1][2] == 'update description'
    assert response.json()[1][3] == 'ok'
    assert response.json()[1][4] == 0

async def test_delete_task(ac: AsyncClient):
    response = await ac.delete('/task/1 test task')
    assert response.status_code == 200
    assert response.json() == {'status': 'success'}
