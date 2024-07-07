import React, { useState, useEffect } from 'react';
import { Box, TextField, Button } from '@mui/material';
import { updateNode } from '../../services/api/layout';
import { fetchTools } from '../../services/api/tools';

const NodeEditor = ({ node, nodes, setNodes }) => {
    console.log(node);
    const [name, setName] = useState(node.name || '');
    const [description, setDescription] = useState(node.description || '');
    const [rolePrompt, setRolePrompt] = useState(node.role_prompt || '');
    const [personalityPrompt, setPersonalityPrompt] = useState(node.personality_prompt || '');
    const [instructionsPrompt, setInstructionsPrompt] = useState(node.instructions_prompt || '');
    const [goalPrompt, setGoalPrompt] = useState(node.goal_prompt || '');
    const [tools, setTools] = useState([]);

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


    const handleSave = async () => {
        try {
            const updatedNode = {
                id: node.id,
                node_type: node.node_type,
                name,
                description,
                role_prompt: rolePrompt,
                personality_prompt: personalityPrompt,
                instructions_prompt: instructionsPrompt,
                goal_prompt: goalPrompt,
                project: node.project
            };
            const data = await updateNode(updatedNode);
            const updatedNodes = nodes.map((n) =>
                n.id === data.id.toString() ? { ...n, data: data } : n
            );
            setNodes(updatedNodes);

        } catch (error) {
            console.error('Error updating node:', error);
        }
    };

    return (
        <Box sx={{ padding: 2 }}>
            <TextField
                label="Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                fullWidth
                margin="normal"
            />
            <TextField
                label="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                rows={4}
            />
            {node.node_type!=="1way"?
            <div>
            <TextField
                label="Role Prompt"
                value={rolePrompt}
                onChange={(e) => setRolePrompt(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                rows={4}
            />
            <TextField
                label="Personality Prompt"
                value={personalityPrompt}
                onChange={(e) => setPersonalityPrompt(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                rows={4}
            />
            <TextField
                label="Instructions Prompt"
                value={instructionsPrompt}
                onChange={(e) => setInstructionsPrompt(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                rows={4}
            />
            <TextField
                label="Goal Prompt"
                value={goalPrompt}
                onChange={(e) => setGoalPrompt(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                rows={4}
            />
            </div>:null}
            <Button variant="contained" color="primary" onClick={handleSave} sx={{ marginTop: 2 }}>
                Save
            </Button>
        </Box>
    );
};

export default NodeEditor;
