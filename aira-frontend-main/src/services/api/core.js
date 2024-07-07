import api from "./api";
// Fetch organizations
const fetchOrganizations = async () => {
    try {
        const response = await api.get('/core/organizations/');
        return response.data;
    } catch (error) {
        console.error('Error fetching organizations:', error);
        throw error;
    }
};

// Create organization
const createOrganization = async (organizationData) => {
    try {
        const response = await api.post('/core/organizations/', organizationData);
        return response.data;
    } catch (error) {
        console.error('Error creating organization:', error);
        throw error;
    }
};

// Fetch projects
const fetchProjects = async () => {
    try {
        const response = await api.get('/core/projects/');
        return response.data;
    } catch (error) {
        console.error('Error fetching projects:', error);
        throw error;
    }
};

// Create project
const createProject = async (projectData) => {
    try {
        const response = await api.post('/core/projects/', projectData);
        return response.data;
    } catch (error) {
        console.error('Error creating project:', error);
        throw error;
    }
};

export { fetchOrganizations, createOrganization, fetchProjects, createProject };