function toggleAccordion(productItem) {
            const content = productItem.querySelector('.accordion-content');
            
            if (content.classList.contains('open')) {
                // Close the accordion
                content.classList.remove('open');
            } else {
                // Close any currently open accordions first (optional but good practice)
                document.querySelectorAll('.accordion-content.open').forEach(openContent => {
                    if (openContent !== content) {
                        openContent.classList.remove('open');
                    }
                });
                
                // Open the accordion
                content.classList.add('open');
            }
        }