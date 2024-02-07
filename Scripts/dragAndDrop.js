const gridItems = document.querySelectorAll('.grid-item img');

gridItems.forEach(item => {
    item.addEventListener('dragstart', handleDragStart);
    item.addEventListener('dragover', handleDragOver);
    item.addEventListener('dragenter', handleDragEnter);
    item.addEventListener('dragleave', handleDragLeave);
    item.addEventListener('drop', handleDrop);
});

let draggedItem = null;

function handleDragStart(event) {
    draggedItem = event.target.parentElement;
}

function handleDragOver(event) {
    event.preventDefault();
}

function handleDragEnter(event) {
    event.target.parentElement.classList.add('drag-over');
}

function handleDragLeave(event) {
    event.target.parentElement.classList.remove('drag-over');
}

function handleDrop(event) {
    event.preventDefault();
    const targetItem = event.target.closest('.grid-item');
    if (draggedItem && targetItem && draggedItem !== targetItem) {
        event.target.parentElement.classList.remove('drag-over');
        const tempContainer = document.createElement('div');
        targetItem.insertAdjacentElement('afterend', tempContainer);
        draggedItem.insertAdjacentElement('beforebegin', targetItem);
        tempContainer.insertAdjacentElement('beforebegin', draggedItem);
        tempContainer.remove();
    }
    draggedItem = null;
}
