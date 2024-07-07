import api from "./api";

// Fetch all tools
const fetchTools = async () => {
    try {
        const response = await api.get('/tools/tools/');
        return response.data;
    } catch (error) {
        console.error('Error fetching tools:', error);
        throw error;
    }
};

// Save tool config
const saveToolConfig = async (node, tool, config) => {
    try {
        const response = await api.post('/tools/tools/save-config/', { node, tool, config });
        return response.data;
    } catch (error) {
        console.error('Error saving tool config:', error);
        throw error;
    }
};

// Get tool config
const getToolConfig = async (nodeId) => {
    try {
        const response = await api.get(`/tools/tools/get-config/?node_id=${nodeId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching tool config:', error);
        throw error;
    }
};

export { fetchTools, saveToolConfig, getToolConfig };
