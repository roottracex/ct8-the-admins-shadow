/*
 * Cybertec8 Access Center
 * Resource loader
 *
 * The frontend requests resources using the user's current scope.
 */

const currentScope = "employee";

async function loadResource(resourceId) {
    const endpoint =
        `/api/resource/${resourceId}?scope=${currentScope}`;

    const response = await fetch(endpoint);

    if (!response.ok) {
        console.log("Resource request failed:", response.status);
        return;
    }

    const data = await response.json();

    console.log("Resource loaded:", data);
}

loadResource(101);