        const gridBtn = document.getElementById('gridBtn');
        const listBtn = document.getElementById('listBtn');
        const mainGrid = document.getElementById('mainGrid');

        // View switching logic
        gridBtn.addEventListener('click', () => {
            gridBtn.classList.add('active');
            listBtn.classList.remove('active');
            mainGrid.classList.remove('list-view');
            mainGrid.classList.add('grid-view');
        });

        listBtn.addEventListener('click', () => {
            listBtn.classList.add('active');
            gridBtn.classList.remove('active');
            mainGrid.classList.remove('grid-view');
            mainGrid.classList.add('list-view');
        });