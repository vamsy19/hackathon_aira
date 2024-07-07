import api from "./api";

// Fetch nodes
const fetchNodes = async () => {
    try {
        const response = await api.get('/layout/nodes/');
        return response.data;
    } catch (error) {
        console.error('Error fetching nodes:', error);
        throw error;
    }
};

// Create node
const createNode = async ({ node_type, name, description, project,entry_node=null }) => {
    const nodeData = {
        node_type,
        name,
        description,
        project,
        entry_node
    };

    try {
        const response = await api.post('/layout/nodes/create/', nodeData);
        return response.data;
    } catch (error) {
        console.error('Error creating node:', error);
        throw error;
    }
};

const getLayout = async (project_id) => {
    try {
        const response = await api.get(`/layout/layout/${project_id}/`);
        return response.data;
    } catch (error) {
        console.error('Error fetching layout:', error);
        throw error;
    }
};


const updateLayout = async (layoutData) => {
    try {
        const response = await api.post('/layout/layout/update/', layoutData);
        return response.data;
    } catch (error) {
        console.error('Error updating layout:', error);
        throw error;
    }
};

const updateNode = async ({ id, node_type, name, description, role_prompt, personality_prompt, instructions_prompt, goal_prompt, project }) => {
    const nodeData = {
        node_type,
        name,
        description,
        role_prompt,
        personality_prompt,
        instructions_prompt,
        goal_prompt,
        project
    };

    try {
        const response = await api.patch(`/layout/nodes/update/${id}/`, nodeData);
        return response.data;
    } catch (error) {
        console.error('Error updating node:', error);
        throw error;
    }
};


const runNode = async (node, msg) => {
    try {
        const response = await api.post('/layout/nodes/run/', { node, msg });
        return response.data;
    } catch (error) {
        console.error('Error running node:', error);
        throw error;
    }
};

const createSuperNode = async ({ entry_node_id, name, description }) => {
    const superNodeData = {
        entry_node_id,
        name,
        description
    };

    try {
        const response = await api.post('/layout/nodes/super/create/', superNodeData);
        return response.data;
    } catch (error) {
        console.error('Error creating super node:', error);
        throw error;
    }
};

const getAllSuperNodes = async () => {
    try {
        const response = await api.get('/layout/nodes/super/');
        return response.data;
    } catch (error) {
        console.error('Error fetching super nodes:', error);
        throw error;
    }
};

export { fetchNodes, createNode, updateLayout, getLayout, updateNode, runNode, createSuperNode, getAllSuperNodes };
