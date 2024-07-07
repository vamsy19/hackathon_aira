import React, { useState, useEffect } from 'react';
import { Box, TextField, Button, MenuItem } from '@mui/material';
import { updateNode } from '../../services/api/layout';
import { fetchTools, saveToolConfig } from '../../services/api/tools';

const NodeConfig = ({ node, nodes, setNodes }) => {
    const [selectedTool, setSelectedTool] = useState(node.tool_instance ? node.tool_instance.tool.id : '');
    const [tools, setTools] = useState([]);
    const [config, setConfig] = useState(node.tool_instance ? JSON.stringify(node.tool_instance.config, null, 2)
        : '');


    useEffect(() => {
        const getTools = async () => {
            try {
                const toolsData = await fetchTools();
                setTools(toolsData);
            } catch (error) {
                console.error('Error fetching tools:', error);
            }
        };

        getTools();

    }, []);


    useEffect(() => {
        if (selectedTool) {
            const tool = tools.find(t => t.id === selectedTool);
            if (tool) {
                if (node.tool_instance && node.tool_instance.tool.id === tool.id) {
                    setConfig(JSON.stringify(node.tool_instance.config, null, 2));
                } else {
                    setConfig(JSON.stringify(tool.config, null, 2));
                }
            } else {
                setConfig('');
            }
        } else {
            setConfig('');
        }
    }, [selectedTool, tools]);


    const handleSave = async () => {
        try {
            const data = await saveToolConfig(node.id, selectedTool, JSON.parse(config));
            // console.log('Tool config saved successfully');
            // console.log(data);
            const updatedNodes = nodes.map((n) =>
                n.id === data.id.toString() ? { ...n, data: data } : n
            );
            setNodes(updatedNodes);
        } catch (error) {
            console.error('Error saving tool config:', error);
        }
    };

    return (
        <Box sx={{ padding: 2 }}>
            <TextField
                select
                label="Tool"
                value={selectedTool}
                onChange={(e) => setSelectedTool(e.target.value)}
                fullWidth
                margin="normal"
            >
                {tools.map((tool) => (
                    <MenuItem key={tool.id} value={tool.id}>
                        {tool.name}
                    </MenuItem>
                ))}
            </TextField>
            <TextField
                label="Config"
                value={config}
                onChange={(e) => setConfig(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                rows={4}
                disabled={!selectedTool}
            />
            <Button variant="contained" color="primary" onClick={handleSave} sx={{ marginTop: 2 }}>
                Save
            </Button>
        </Box>
    );
};

export default NodeConfig;
